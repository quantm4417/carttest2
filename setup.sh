#!/bin/bash
# First-time setup script for Dampfi Gallery

set -e

echo "=========================================="
echo "Dampfi Gallery - First Time Setup"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env and set your SECRET_KEY"
    echo ""
fi

# Create data directories
echo "Creating data directories..."
mkdir -p data/uploads
mkdir -p data/images
echo "Directories created."
echo ""

# Initialize database
echo "Initializing database..."
python scripts/init_db.py
echo ""

# Check Docker
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "Docker and Docker Compose found."
    echo ""
    echo "To start the application:"
    echo "  docker-compose up -d"
    echo ""
    echo "To view logs:"
    echo "  docker-compose logs -f"
    echo ""
else
    echo "Docker not found. You can run the app directly with:"
    echo "  python -m flask run"
    echo ""
fi

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Start the application (Docker or Flask directly)"
echo "2. Open http://localhost:5000 in your browser"
echo "3. Configure user credentials (1-5) via the UI"
echo "4. Add products in Product Management"
echo ""



