from flask import Flask
from app.config import Config
from app.database import init_db
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure upload directory exists with proper permissions
    upload_folder = app.config['UPLOAD_FOLDER']
    db_path = app.config['DATABASE_PATH']
    db_dir = os.path.dirname(db_path)
    
    os.makedirs(upload_folder, exist_ok=True)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    
    # Set directory permissions (read/write/execute for owner, read/execute for group/others)
    try:
        if os.path.exists(upload_folder):
            os.chmod(upload_folder, 0o755)
        if db_dir and os.path.exists(db_dir):
            os.chmod(db_dir, 0o755)
        # Set database file permissions if it exists
        if os.path.exists(db_path):
            os.chmod(db_path, 0o644)
    except Exception as e:
        print(f"Warning: Could not set permissions: {e}")
    
    # Initialize database
    init_db()
    
    # Register blueprints
    from app.routes.views import bp as views_bp
    from app.routes.api import bp as api_bp
    
    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app



