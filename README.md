j# Installation

```console
$ pip install probe-internet
```

## Usage

Define a `profile.toml` similar to:

```toml
[probe]
ip = "8.8.8.8"
port = 53
timeout = 3
interval = 5

[twilio]
account_sid = "..."
auth_token = "..."
source_phone_number = "+1..."
target_phone_number = "+1..."
```

Run it:

```console
$ probe-internet
```
