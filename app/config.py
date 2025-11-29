import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or os.path.join(
        Path(__file__).parent.parent, 'data', 'database.db'
    )
    
    # Uploads
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(
        Path(__file__).parent.parent, 'data', 'uploads'
    )
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_UPLOAD_SIZE', 10485760))  # 10MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    # Dampfi.ch
    DAMPFI_BASE_URL = 'https://www.dampfi.ch'
    
    # Playwright
    PLAYWRIGHT_HEADLESS = True
    PLAYWRIGHT_TIMEOUT = 30000  # 30 seconds



