from flask import Blueprint, request, jsonify
from app.models import (
    create_product, update_product, get_product_by_id, get_all_products,
    get_user_by_id, update_user_credentials, get_user_orders
)
from app.utils.validators import is_valid_dampfi_url, validate_user_id
from app.utils.helpers import save_uploaded_file, delete_image_file
from app.services.scraper import scrape_product_metadata
from app.services.automation import run_checkout
from app.database import log_message, get_db
import json

bp = Blueprint('api', __name__)

@bp.route('/products', methods=['GET'])
def list_products():
    """Get all products"""
    products = get_all_products()
    return jsonify({'products': products})

@bp.route('/products', methods=['POST'])
def create_product_endpoint():
    """Create a new product"""
    data = request.get_json() or {}
    product_url = data.get('product_url', '').strip()
    
    if not product_url:
        return jsonify({'error': 'Product URL is required'}), 400
    
    if not is_valid_dampfi_url(product_url):
        return jsonify({'error': 'Invalid dampfi.ch URL'}), 400
    
    # Check if product already exists
    products = get_all_products()
    for p in products:
        if p['product_url'] == product_url:
            return jsonify({'error': 'Product with this URL already exists'}), 400
    
    product_id = create_product(
        product_url=product_url,
        name=data.get('name', 'Unknown Product'),
        price=data.get('price'),
        stock_status=data.get('stock_status', 'unknown'),
        options=data.get('options')
    )
    
    if product_id:
        product = get_product_by_id(product_id)
        return jsonify({'product': product}), 201
    else:
        return jsonify({'error': 'Failed to create product'}), 500

@bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get product by ID"""
    product = get_product_by_id(product_id)
    if product:
        return jsonify({'product': product})
    return jsonify({'error': 'Product not found'}), 404

@bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product_endpoint(product_id):
    """Update a product"""
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.get_json() or {}
    updates = {}
    
    # Validate URL if provided
    if 'product_url' in data:
        url = data['product_url'].strip()
        if not is_valid_dampfi_url(url):
            return jsonify({'error': 'Invalid dampfi.ch URL'}), 400
        updates['product_url'] = url
    
    if 'name' in data:
        updates['name'] = data['name']
    if 'price' in data:
        updates['price'] = data.get('price')
    if 'stock_status' in data:
        updates['stock_status'] = data['stock_status']
    if 'options' in data:
        updates['options'] = data['options']
    
    if update_product(product_id, **updates):
        product = get_product_by_id(product_id)
        return jsonify({'product': product})
    else:
        return jsonify({'error': 'Failed to update product'}), 500

@bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Delete image file
    if product.get('image_path'):
        delete_image_file(product['image_path'])
    
    # Delete from database
    from app.database import get_db
    conn = get_db()
    try:
        conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        return jsonify({'message': 'Product deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@bp.route('/products/<int:product_id>/scrape', methods=['POST'])
def scrape_product(product_id):
    """Trigger metadata scraping for a product"""
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Retry logic
    max_retries = 2
    result = None
    
    for attempt in range(max_retries):
        result = scrape_product_metadata(product['product_url'])
        
        if 'error' not in result:
            # Update product with scraped data
            updates = {}
            if result.get('name'):
                updates['name'] = result['name']
            if result.get('price') is not None:
                updates['price'] = result['price']
            if result.get('stock_status'):
                updates['stock_status'] = result['stock_status']
            if result.get('options') is not None:
                updates['options'] = result['options']
            
            if updates:
                update_product(product_id, **updates)
            
            return jsonify({'product': get_product_by_id(product_id), 'scraped': result})
        
        if attempt < max_retries - 1:
            log_message('info', f'Retrying scrape for product {product_id}', {'attempt': attempt + 1})
    
    # Both attempts failed
    error_msg = result.get('error', 'Unknown error')
    if 'timeout' in error_msg.lower() or 'connection' in error_msg.lower():
        error_msg = 'dampfi.ch appears to be down'
    
    return jsonify({'error': error_msg}), 500

@bp.route('/products/<int:product_id>/upload', methods=['POST'])
def upload_product_image(product_id):
    """Upload product image"""
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Delete old image if exists
    if product.get('image_path'):
        delete_image_file(product['image_path'])
    
    # Save new image
    image_path = save_uploaded_file(file, product_id)
    if image_path:
        update_product(product_id, image_path=image_path)
        product = get_product_by_id(product_id)
        return jsonify({'product': product}), 200
    else:
        return jsonify({'error': 'Invalid file type or upload failed'}), 400

@bp.route('/user/<int:user_id>/credentials', methods=['POST'])
def save_user_credentials(user_id):
    """Save user's dampfi.ch credentials"""
    if not validate_user_id(user_id):
        return jsonify({'error': 'Invalid user ID'}), 400
    
    data = request.get_json() or {}
    dampfi_email = data.get('dampfi_email', '').strip()
    dampfi_password = data.get('dampfi_password', '').strip()
    
    if not dampfi_email or not dampfi_password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    if update_user_credentials(user_id, dampfi_email, dampfi_password):
        return jsonify({'message': 'Credentials saved successfully'}), 200
    else:
        return jsonify({'error': 'Failed to save credentials'}), 500

@bp.route('/checkout/confirm', methods=['POST'])
def confirm_checkout():
    """Confirm and execute checkout"""
    data = request.get_json() or {}
    user_id = data.get('user_id')
    selected_items = data.get('items', [])
    
    if not user_id or not validate_user_id(user_id):
        return jsonify({'error': 'Invalid user ID'}), 400
    
    if not selected_items:
        return jsonify({'error': 'No items selected'}), 400
    
    user = get_user_by_id(user_id)
    if not user or not user.get('dampfi_email') or not user.get('dampfi_password'):
        return jsonify({'error': 'User credentials not configured'}), 400
    
    # Run checkout automation
    result = run_checkout(
        user_id=user_id,
        user_credentials={
            'dampfi_email': user['dampfi_email'],
            'dampfi_password': user['dampfi_password']
        },
        selected_items=selected_items
    )
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@bp.route('/user/<int:user_id>/orders', methods=['GET'])
def get_orders(user_id):
    """Get user orders"""
    if not validate_user_id(user_id):
        return jsonify({'error': 'Invalid user ID'}), 400
    
    orders = get_user_orders(user_id)
    return jsonify({'orders': orders})

@bp.route('/logs', methods=['GET'])
def get_logs():
    """Get logs (debug mode)"""
    debug_mode = request.args.get('debug', 'false').lower() == 'true'
    if not debug_mode:
        return jsonify({'error': 'Debug mode not enabled'}), 403
    
    limit = request.args.get('limit', 100, type=int)
    conn = get_db()
    try:
        rows = conn.execute(
            'SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?',
            (limit,)
        ).fetchall()
        logs = []
        for row in rows:
            log_entry = dict(row)
            if log_entry.get('context'):
                log_entry['context'] = json.loads(log_entry['context'])
            logs.append(log_entry)
        return jsonify({'logs': logs})
    finally:
        conn.close()



