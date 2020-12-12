# Installation

```console
$ pip install probe-internet
```

## Usage

Define a `profile.toml` similar to:

```toml
[probe]
ip = "8.8.8.8"
port = 53

# how often to probe
interval = 5
timeout = 3

[twilio]
account_sid = "..."
auth_token = "..."
source_phone_number = "+1..."
target_phone_number = "+1..."

# how long must the connection be down before a message is sent
min_interval = 30
```

Run it:

```console
$ probe-internet
```
