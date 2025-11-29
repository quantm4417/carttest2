#!/bin/bash
# Fix database and upload directory permissions

echo "Fixing permissions for Dampfi Gallery..."

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Fix data directory permissions
if [ -d "$PROJECT_DIR/data" ]; then
    echo "Setting permissions for data directory..."
    chmod -R 755 "$PROJECT_DIR/data"
    
    # Fix database file permissions if it exists
    if [ -f "$PROJECT_DIR/data/database.db" ]; then
        chmod 644 "$PROJECT_DIR/data/database.db"
        echo "Database file permissions fixed."
    fi
    
    # Fix uploads directory
    if [ -d "$PROJECT_DIR/data/uploads" ]; then
        chmod -R 755 "$PROJECT_DIR/data/uploads"
        echo "Uploads directory permissions fixed."
    fi
else
    echo "Creating data directory..."
    mkdir -p "$PROJECT_DIR/data/uploads"
    chmod -R 755 "$PROJECT_DIR/data"
fi

echo "Permissions fixed!"
echo ""
echo "If you still have issues, make sure you own the files:"
echo "  sudo chown -R \$USER:\$USER $PROJECT_DIR/data"

