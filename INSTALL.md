# Installation Guide

## Quick Installation

After cloning the repository:

```bash
# 1. Make scripts executable
chmod +x install_setup.sh start.sh

# 2. Run installation
./install_setup.sh

# 3. Start the application
./start.sh
```

That's it! The application will be available at http://localhost:5000

## What the Installation Does

The `install_setup.sh` script automatically:

1. ✅ Checks Python 3 and pip
2. ✅ Installs system dependencies (Playwright requirements)
3. ✅ Creates Python virtual environment
4. ✅ Installs all Python packages
5. ✅ Installs Playwright browsers
6. ✅ Creates `.env` file with auto-generated SECRET_KEY
7. ✅ Creates data directories
8. ✅ Initializes database with 5 default users
9. ✅ Sets proper file permissions

## Manual Installation (if script fails)

If you prefer to install manually:

```bash
# 1. Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv wget gnupg ca-certificates \
    fonts-liberation libasound2t64 libatk-bridge2.0-0t64 libatk1.0-0t64 \
    libatspi2.0-0t64 libcups2t64 libdbus-1-3 libdrm2 libgbm1 libgtk-3-0t64 \
    libnspr4 libnss3 libwayland-client0 libxcomposite1 libxdamage1 \
    libxfixes3 libxkbcommon0 libxrandr2 xdg-utils libu2f-udev libvulkan1

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# 4. Install Playwright
playwright install chromium

# 5. Create .env file
cp .env.example .env
# Edit .env and set SECRET_KEY (or generate: openssl rand -hex 32)

# 6. Initialize database
python3 scripts/init_db.py
```

## Troubleshooting

### Permission Errors

If you get database permission errors:

```bash
chmod -R 755 data/
chmod 644 data/database.db
```

### Port Already in Use

If port 5000 is already in use, edit `run.py` and change the port:

```python
app.run(host='0.0.0.0', port=8080, debug=True)  # Use port 8080 instead
```

### Virtual Environment Issues

If the virtual environment is corrupted:

```bash
rm -rf venv
./install_setup.sh  # Run installation again
```

## After Installation

1. Start the app: `./start.sh`
2. Open http://localhost:5000
3. Configure user credentials (1-5)
4. Add products in Product Management

