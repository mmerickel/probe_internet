import argparse
from datetime import datetime
from humanize import naturaldelta
import logging
import socket
import sys
import time
import toml
from twilio.rest import Client as TwilioClient

log = logging.getLogger(__name__)

def notify_sms(
    lost_time,
    account_id,
    auth_token,
    source_phone_number,
    target_phone_number,
    min_interval=0,
):
    lost_duration = datetime.utcnow() - lost_time
    if lost_duration.total_seconds() < min_interval:
        log.info('skipping sms, internet was not out long enough')
        return
    lost_duration = naturaldelta(lost_duration)
    body = (
        'Internet dropped at {} ({}).'
        .format(lost_time, lost_duration)
    )

    try:
        twilio = TwilioClient(account_id, auth_token)
        twilio.messages.create(
            body=body,
            from_=source_phone_number,
            to=target_phone_number,
        )
    except Exception:
        log.exception('squashing error sending sms')

def probe_internet(host, port, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        log.debug('probing {}:{}'.format(host, port))
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        log.debug('probe failed={}'.format(ex))
        return False

def runloop(probe, probe_interval=5, notifier=None):
    lost_time = None
    while True:
        start = datetime.utcnow()
        result = probe()
        if result:
            if lost_time is not None:
                log.info('internet is back!')
                if notifier is not None:
                    notifier(lost_time)
                lost_time = None
            else:
                log.debug('internet is up')
        elif lost_time is None:
            lost_time = start
            log.warn('internet is out')
        else:
            log.info('internet still out')
        delay = probe_interval - (datetime.utcnow() - start).total_seconds()
        if delay > 0:
            time.sleep(delay)

def parse_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--profile', default='profile.toml')
    opts = parser.parse_args(args)
    return opts

def main(args=sys.argv[1:]):
    opts = parse_options(args)
    logging.basicConfig(
        level=logging.DEBUG if opts.verbose else logging.INFO,
        format='%(asctime)-15s %(levelname)-8s [%(name)s] %(message)s',
    )
    with open(opts.profile, 'r') as fp:
        profile = toml.load(fp)
    def probe():
        return probe_internet(
            profile['probe']['ip'],
            port=profile['probe']['port'],
            timeout=profile['probe']['timeout'],
        )
    def notifier(lost_time):
        notify_sms(
            lost_time,
            profile['twilio']['account_sid'],
            profile['twilio']['auth_token'],
            profile['twilio']['source_phone_number'],
            profile['twilio']['target_phone_number'],
            profile['twilio'].get('min_interval', 0),
        )
    runloop(probe, profile['probe']['interval'], notifier)

if __name__ == '__main__':
    sys.exit(main())
