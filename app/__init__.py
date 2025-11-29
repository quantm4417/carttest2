from flask import Flask
from app.config import Config
from app.database import init_db
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.dirname(app.config['DATABASE_PATH']), exist_ok=True)
    
    # Initialize database
    init_db()
    
    # Register blueprints
    from app.routes.views import bp as views_bp
    from app.routes.api import bp as api_bp
    
    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app



