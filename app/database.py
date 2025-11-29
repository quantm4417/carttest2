import sqlite3
import json
import os
from datetime import datetime
from app.config import Config

def get_db():
    """Get database connection"""
    # Ensure database directory exists and has proper permissions
    db_path = Config.DATABASE_PATH
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
        # Set directory permissions (read/write/execute for owner)
        try:
            os.chmod(db_dir, 0o755)
        except:
            pass  # Ignore if chmod fails
    
    # Connect to database
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    
    # Ensure database file has write permissions
    try:
        if os.path.exists(db_path):
            os.chmod(db_path, 0o644)
    except:
        pass  # Ignore if chmod fails
    
    return conn

def create_tables():
    """Create all database tables"""
    conn = get_db()
    try:
        # Users table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT,
                email TEXT,
                dampfi_email TEXT,
                dampfi_password TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Products table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_url TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                price REAL,
                stock_status TEXT DEFAULT 'unknown',
                options TEXT,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Orders table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_price REAL,
                items TEXT,
                status TEXT DEFAULT 'pending',
                confirmation_data TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Logs table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                context TEXT
            )
        ''')
        
        conn.commit()
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise
    finally:
        conn.close()

def init_db():
    """Initialize database with tables"""
    create_tables()

def log_message(level, message, context=None):
    """Log a message to the database"""
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO logs (timestamp, level, message, context) VALUES (?, ?, ?, ?)',
            (datetime.utcnow().isoformat(), level, message, json.dumps(context) if context else None)
        )
        conn.commit()
    except Exception as e:
        print(f"Error logging message: {e}")
    finally:
        conn.close()
