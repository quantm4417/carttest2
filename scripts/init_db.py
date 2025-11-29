#!/usr/bin/env python3
"""
Initialize the database and run setup
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db
from app.config import Config
from scripts.seed_users import seed_users

def setup():
    """Initialize database and seed users"""
    print("Initializing database...")
    init_db()
    print("Database initialized.")
    
    print("\nSeeding users...")
    seed_users()
    
    print("\nCreating directories...")
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(Config.UPLOAD_FOLDER), 'images'), exist_ok=True)
    print("Directories created.")
    
    print("\nSetup complete!")
    print(f"Database: {Config.DATABASE_PATH}")
    print(f"Upload folder: {Config.UPLOAD_FOLDER}")

if __name__ == '__main__':
    setup()



