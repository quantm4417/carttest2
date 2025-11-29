#!/bin/bash
# Complete installation and setup script for Dampfi Gallery
# Run this once after cloning the repository

set -e

echo "=========================================="
echo "Dampfi Gallery - Installation & Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! python3 --version; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

# Check if pip is installed
echo "Checking pip..."
if ! python3 -m pip --version; then
    echo "ERROR: pip is not installed"
    exit 1
fi

# Install system dependencies for Playwright (Ubuntu/Debian)
echo ""
echo "Installing system dependencies for Playwright..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    # Ubuntu 24.04+ uses t64 transitional packages
    sudo apt-get install -y \
        python3-pip \
        python3-venv \
        wget \
        gnupg \
        ca-certificates \
        fonts-liberation \
        libasound2t64 \
        libatk-bridge2.0-0t64 \
        libatk1.0-0t64 \
        libatspi2.0-0t64 \
        libcups2t64 \
        libdbus-1-3 \
        libdrm2 \
        libgbm1 \
        libgtk-3-0t64 \
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
    echo "Virtual environment already exists. Skipping..."
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Install Playwright browsers
echo ""
echo "Installing Playwright browsers..."
playwright install chromium

# Create .env file if it doesn't exist
echo ""
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
    else
        # Create basic .env file
        cat > .env << EOF
FLASK_APP=app
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
# DATABASE_PATH and UPLOAD_FOLDER use relative paths by default
# Uncomment and set if you want custom paths:
# DATABASE_PATH=./data/database.db
# UPLOAD_FOLDER=./data/uploads
MAX_UPLOAD_SIZE=10485760
EOF
    fi
    echo "✓ .env file created with generated SECRET_KEY"
else
    echo "✓ .env file already exists."
fi

# Create data directories with proper permissions
echo ""
echo "Creating data directories..."
mkdir -p data/uploads
mkdir -p data/images
chmod -R 755 data/
echo "✓ Directories created with proper permissions."

# Initialize database
echo ""
echo "Initializing database..."
python3 scripts/init_db.py

# Set final permissions
echo ""
echo "Setting final permissions..."
chmod -R 755 data/
if [ -f data/database.db ]; then
    chmod 644 data/database.db
fi
chmod +x start.sh
chmod +x install_setup.sh

echo ""
echo "=========================================="
echo "✓ Installation complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Start the application: ./start.sh"
echo "  2. Open http://localhost:5000 in your browser"
echo "  3. Configure user credentials (1-5) via the UI"
echo "  4. Add products in Product Management"
echo ""
echo "To start the app, run: ./start.sh"
echo ""

