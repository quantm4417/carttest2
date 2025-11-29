import re
from urllib.parse import urlparse
from app.config import Config

def is_valid_dampfi_url(url):
    """Validate that URL is a valid dampfi.ch product URL"""
    try:
        parsed = urlparse(url)
        if parsed.netloc not in ['www.dampfi.ch', 'dampfi.ch']:
            return False
        if not parsed.path or parsed.path == '/':
            return False
        return True
    except:
        return False

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_user_id(user_id):
    """Validate user ID is between 1 and 5"""
    try:
        uid = int(user_id)
        return 1 <= uid <= 5
    except:
        return False



