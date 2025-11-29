#!/bin/bash
# Start script for Dampfi Gallery (Native Linux)

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run ./install_setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo "WARNING: .env file not found. Creating basic .env..."
    cat > .env << EOF
FLASK_APP=app
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
MAX_UPLOAD_SIZE=10485760
EOF
    echo "✓ Created .env file with generated SECRET_KEY"
fi

# Ensure data directories exist
mkdir -p data/uploads
mkdir -p data/images
chmod -R 755 data/ 2>/dev/null || true

# Start Flask application
echo "=========================================="
echo "Starting Dampfi Gallery..."
echo "=========================================="
echo ""
echo "Application: http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

python3 run.py

