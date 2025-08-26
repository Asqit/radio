# Radio

Continuous internet radio streaming daemon for Raspberry Pi.

## Requirements

- Raspberry Pi (Debian/Ubuntu)
- Python 3
- Internet connection
- Audio output configured

## Setup

1. Add your stream URL to `url.txt`
   ```bash
   echo "https://your-radio-stream-url" > url.txt
   ```
2. Make installer executable and run:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

## What it does

- Installs mplayer via apt
- Creates systemd service
- Starts radio daemon automatically
- Monitors network connectivity
- Restarts stream on failures

## Features

- Auto-recovery from network interrupts
- Starts on boot via systemd
- ~20MB RAM usage
- Silent operation (no console output)
- Validates stream URLs
- Max 10 retry attempts on network failure

## Control

```bash
sudo systemctl status radio   # Check status
sudo systemctl stop radio     # Stop
sudo systemctl start radio    # Start
sudo systemctl restart radio  # Restart
sudo systemctl disable radio  # Disable auto-start
```

## Logs

```bash
sudo journalctl -u radio -f   # Follow logs
sudo journalctl -u radio      # View all logs
```

## Troubleshooting

- **No audio**: Check `alsamixer` or audio output settings
- **Stream fails**: Verify URL in `url.txt` is valid
- **Service won't start**: Check logs with `journalctl -u radio`
