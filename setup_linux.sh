#!/bin/bash
# Native Linux setup script for Dampfi Gallery

set -e

echo "=========================================="
echo "Dampfi Gallery - Linux Native Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "ERROR: Python 3 is not installed"; exit 1; }

# Check if pip is installed
echo "Checking pip..."
python3 -m pip --version || { echo "ERROR: pip is not installed"; exit 1; }

# Install system dependencies for Playwright (Ubuntu/Debian)
echo ""
echo "Installing system dependencies for Playwright..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y \
        python3-pip \
        python3-venv \
        wget \
        gnupg \
        ca-certificates \
        fonts-liberation \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libatspi2.0-0 \
        libcups2 \
        libdbus-1-3 \
        libdrm2 \
        libgbm1 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libwayland-client0 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
        libxkbcommon0 \
        libxrandr2 \
        xdg-utils \
        libu2f-udev \
        libvulkan1
elif command -v yum &> /dev/null; then
    sudo yum install -y \
        python3-pip \
        wget \
        ca-certificates \
        liberation-fonts \
        alsa-lib \
        atk \
        cups-libs \
        dbus-glib \
        gtk3 \
        libdrm \
        libXcomposite \
        libXdamage \
        libXfixes \
        libxkbcommon \
        libXrandr \
        mesa-libgbm \
        nss \
        xorg-x11-utils
else
    echo "WARNING: Could not detect package manager. Please install Playwright dependencies manually."
fi

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo ""
echo "Installing Playwright browsers..."
playwright install chromium

# Create .env file if it doesn't exist
echo ""
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env and set your SECRET_KEY"
    echo "You can generate a secret key with: openssl rand -hex 32"
else
    echo ".env file already exists."
fi

# Create data directories
echo ""
echo "Creating data directories..."
mkdir -p data/uploads
mkdir -p data/images
echo "Directories created."

# Initialize database
echo ""
echo "Initializing database..."
python3 scripts/init_db.py

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: python3 run.py"
echo "     OR: python3 -m flask run"
echo ""
echo "The application will be available at: http://localhost:5000"
echo ""
echo "Next steps:"
echo "  1. Configure user credentials (1-5) via the UI"
echo "  2. Add products in Product Management"
echo ""

