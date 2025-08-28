#!/bin/bash
set -e

# Figure out the real user (not root if run with sudo)
REAL_USER=${SUDO_USER:-$USER}

# Resolve absolute path of this script (so service always knows where to run)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Install mplayer
echo "Installing mplayer..."
sudo apt-get update
sudo apt-get install -y mplayer

# Create systemd service
echo "Creating systemd service..."
sudo tee /etc/systemd/system/radio.service > /dev/null <<EOF
[Unit]
Description=Radio Streaming Daemon
After=network.target

[Service]
Type=simple
User=${REAL_USER}
WorkingDirectory=${SCRIPT_DIR}
ExecStart=/usr/bin/python3 ${SCRIPT_DIR}/daemon.py
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable radio.service
sudo systemctl restart radio.service

echo "Installation complete. Radio daemon is now running."
echo "Use: sudo systemctl status radio"
echo "Logs: journalctl -u radio -f"
