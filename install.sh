#!/bin/bash

# MKC - Mobile Number Kali Tracker Installation Script
# This script installs MKC and all its dependencies

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    MKC - Mobile Number Kali Tracker                    ║"
echo "║                    Installation Script                        ║"
echo "║                    Version 1.0                               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "[WARNING] This script should not be run as root!"
   echo "[INFO] Please run as a regular user."
   exit 1
fi

# Check Python version
echo "[INFO] Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "[ERROR] Python 3 is not installed!"
    echo "[INFO] Please install Python 3.7+ first."
    exit 1
fi

# Check pip
echo "[INFO] Checking pip..."
python3 -m pip --version
if [ $? -ne 0 ]; then
    echo "[ERROR] pip is not installed!"
    echo "[INFO] Please install pip first."
    exit 1
fi

# Install dependencies
echo ""
echo "[INFO] Installing Python dependencies..."
python3 -m pip install --user -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies!"
    echo "[INFO] Try running: pip3 install --user -r requirements.txt"
    exit 1
fi

# Make script executable
echo "[INFO] Making MKC executable..."
chmod +x mkc.py

# Create symlink for global access (optional)
echo ""
echo "[QUESTION] Do you want to create a global symlink? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "[INFO] Creating global symlink..."
    sudo ln -sf "$(pwd)/mkc.py" /usr/local/bin/mkc
    echo "[SUCCESS] You can now run 'mkc' from anywhere!"
else
    echo "[INFO] No global symlink created."
    echo "[INFO] Run with: python3 mkc.py"
fi

# Test installation
echo ""
echo "[INFO] Testing installation..."
python3 mkc.py help

if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    INSTALLATION SUCCESSFUL!                    ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "[SUCCESS] MKC has been installed successfully!"
    echo ""
    echo "[USAGE] Run the tool with:"
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "  mkc help"
        echo "  mkc track 9876543210"
    else
        echo "  python3 mkc.py help"
        echo "  python3 mkc.py track 9876543210"
    fi
    echo ""
    echo "[INFO] Check README.md for detailed usage instructions."
else
    echo "[ERROR] Installation test failed!"
    echo "[INFO] Please check the error messages above."
    exit 1
fi

echo ""
echo "[INFO] Installation completed!" 