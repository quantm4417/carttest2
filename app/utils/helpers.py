import os
from werkzeug.utils import secure_filename
from app.config import Config
from app.utils.validators import allowed_file

def save_uploaded_file(file, product_id=None):
    """Save uploaded file and return the path"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add product ID prefix if provided
        if product_id:
            name, ext = os.path.splitext(filename)
            filename = f"{product_id}_{name}{ext}"
        
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filepath
    return None

def delete_image_file(image_path):
    """Delete an image file"""
    if image_path and os.path.exists(image_path):
        try:
            os.remove(image_path)
            return True
        except Exception as e:
            print(f"Error deleting image: {e}")
            return False
    return False



