#!/bin/bash
set -e

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
User=$USER
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 $(pwd)/daemon.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable radio.service
sudo systemctl start radio.service

echo "Installation complete. Radio daemon is now running."
echo "Use 'sudo systemctl status radio' to check status."