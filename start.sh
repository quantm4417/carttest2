#!/bin/bash
# Start script for Dampfi Gallery (Native Linux)

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "WARNING: .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "Please edit .env and set your SECRET_KEY"
fi

# Start Flask application
echo "Starting Dampfi Gallery..."
echo "Application will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

python3 run.py

