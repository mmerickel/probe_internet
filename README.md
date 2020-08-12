## Usage

1.  Install Dependencies

```console
$ poetry install
```

2. Define a `profile.toml` similar to:

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

3. Run it:

```console
$ poetry run python -m probe_internet
```
