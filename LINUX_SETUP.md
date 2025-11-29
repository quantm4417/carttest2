# Native Linux Setup Guide

This guide will help you set up and run Dampfi Gallery natively on Linux (without Docker).

## Prerequisites

- **Python 3.11+** (check with `python3 --version`)
- **pip** (usually comes with Python)
- **System packages** for Playwright (will be installed by setup script)

## Quick Start

### 1. Run Setup Script

```bash
chmod +x setup_linux.sh
./setup_linux.sh
```

This script will:
- Install system dependencies for Playwright
- Create a Python virtual environment
- Install all Python packages
- Install Playwright browsers
- Create `.env` file
- Initialize the database

### 2. Configure Environment

Edit `.env` file and set a strong `SECRET_KEY`:

```bash
nano .env
```

Generate a secret key:
```bash
openssl rand -hex 32
```

### 3. Start the Application

**Option A: Using the start script**
```bash
chmod +x start.sh
./start.sh
```

**Option B: Manual start**
```bash
# Activate virtual environment
source venv/bin/activate

# Start Flask
python3 run.py
# OR
python3 -m flask run
```

The application will be available at: **http://localhost:5000**

## Manual Setup (if script doesn't work)

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
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
```

**Fedora/RHEL:**
```bash
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
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install chromium
```

### 5. Configure Environment

```bash
cp .env.example .env
nano .env  # Edit and set SECRET_KEY
```

### 6. Initialize Database

```bash
python3 scripts/init_db.py
```

### 7. Start Application

```bash
python3 run.py
```

## Running as a Service (Systemd)

To run the application as a systemd service:

### 1. Create Service File

```bash
sudo nano /etc/systemd/system/dampfi.service
```

Add this content (adjust paths as needed):

```ini
[Unit]
Description=Dampfi Gallery Application
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/dampfi
Environment="PATH=/path/to/dampfi/venv/bin"
ExecStart=/path/to/dampfi/venv/bin/python3 /path/to/dampfi/run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable dampfi
sudo systemctl start dampfi
```

### 3. Check Status

```bash
sudo systemctl status dampfi
```

## Troubleshooting

### Playwright Issues

If Playwright fails to run:
```bash
# Reinstall browsers
playwright install chromium --force

# Check dependencies
playwright install-deps chromium
```

### Permission Issues

If you get permission errors:
```bash
# Make scripts executable
chmod +x setup_linux.sh start.sh

# Fix data directory permissions
chmod -R 755 data/
```

### Port Already in Use

If port 5000 is already in use:
```bash
# Find what's using the port
sudo lsof -i :5000

# Or change port in run.py
# Change: app.run(host='0.0.0.0', port=5000)
```

### Database Issues

If database errors occur:
```bash
# Remove old database
rm data/database.db

# Reinitialize
python3 scripts/init_db.py
```

## Development Mode

For development with auto-reload:

```bash
source venv/bin/activate
export FLASK_ENV=development
export FLASK_DEBUG=1
python3 -m flask run
```

## Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

Or use a reverse proxy (nginx) in front of Gunicorn for better performance.

