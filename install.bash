#!/bin/bash

APP_NAME="uxcomdline"
INSTALL_DIR="/usr/local/bin"
SOURCE_FILE="uxcomdline.py"

echo "=== Installing $APP_NAME ==="

# Python 3 kontrolü
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Kaynak dosya kontrolü
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: $SOURCE_FILE not found in current directory."
    exit 1
fi

# Çalıştırılabilir yap ve /usr/local/bin dizinine kopyala
chmod +x "$SOURCE_FILE"
echo "Copying $SOURCE_FILE to $INSTALL_DIR/$APP_NAME..."
sudo cp "$SOURCE_FILE" "$INSTALL_DIR/$APP_NAME"

if [ $? -eq 0 ]; then
    echo "----------------------------------------"
    echo "Installation successful!"
    echo "You can now run '$APP_NAME --help' from anywhere."
    echo "----------------------------------------"
else
    echo "Error: Installation failed. Make sure you have sudo privileges."
    exit 1
fi