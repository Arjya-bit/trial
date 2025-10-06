#!/bin/bash
# Stealth Loader for Linux
# Launches OT-AFP Platform with stealth options

echo "Starting Ultimate OT-AFP Platform..."

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
    echo "Requesting root privileges..."
    sudo "$0" "$@"
    exit
fi

# Set working directory
INSTALL_DIR="/opt/ot-afp"

# Create directory if not exists
mkdir -p "$INSTALL_DIR"

# Copy files if needed
if [ -d "./backend" ]; then
    cp -r ./backend "$INSTALL_DIR/"
fi

# Start backend
cd "$INSTALL_DIR/backend" || exit
python3 main.py &

echo "OT-AFP Platform started"
echo "PID: $!"
