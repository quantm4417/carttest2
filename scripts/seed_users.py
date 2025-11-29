#!/usr/bin/env python3
"""
Seed the database with 5 default user accounts
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_db
from app.config import Config

def seed_users():
    """Create 5 default user accounts"""
    conn = get_db()
    try:
        # Check if users already exist
        existing = conn.execute('SELECT COUNT(*) as count FROM users').fetchone()
        if existing['count'] > 0:
            print("Users already exist. Skipping seed.")
            return
        
        # Create 5 users
        users = [
            {'username': 'user1', 'email': 'user1@example.com'},
            {'username': 'user2', 'email': 'user2@example.com'},
            {'username': 'user3', 'email': 'user3@example.com'},
            {'username': 'user4', 'email': 'user4@example.com'},
            {'username': 'user5', 'email': 'user5@example.com'},
        ]
        
        for user in users:
            conn.execute('''
                INSERT INTO users (username, email)
                VALUES (?, ?)
            ''', (user['username'], user['email']))
        
        conn.commit()
        print(f"Successfully created {len(users)} user accounts.")
        print("Note: Users need to configure their dampfi.ch credentials via the UI.")
        
    except Exception as e:
        print(f"Error seeding users: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    seed_users()



