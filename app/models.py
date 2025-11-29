from app.database import get_db
import json
import sqlite3
from datetime import datetime

def get_product_by_id(product_id):
    """Get product by ID"""
    conn = get_db()
    try:
        row = conn.execute(
            'SELECT * FROM products WHERE id = ?', (product_id,)
        ).fetchone()
        if row:
            product = dict(row)
            if product.get('options'):
                product['options'] = json.loads(product['options'])
            return product
        return None
    finally:
        conn.close()

def get_all_products():
    """Get all products"""
    conn = get_db()
    try:
        rows = conn.execute(
            'SELECT * FROM products ORDER BY created_at DESC'
        ).fetchall()
        products = []
        for row in rows:
            product = dict(row)
            if product.get('options'):
                product['options'] = json.loads(product['options'])
            products.append(product)
        return products
    finally:
        conn.close()

def create_product(product_url, name, price=None, stock_status='unknown', options=None, image_path=None):
    """Create a new product"""
    conn = get_db()
    try:
        options_json = json.dumps(options) if options else None
        conn.execute('''
            INSERT INTO products (product_url, name, price, stock_status, options, image_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (product_url, name, price, stock_status, options_json, image_path))
        conn.commit()
        return conn.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def update_product(product_id, **kwargs):
    """Update product fields"""
    conn = get_db()
    try:
        updates = []
        values = []
        
        if 'product_url' in kwargs:
            updates.append('product_url = ?')
            values.append(kwargs['product_url'])
        if 'name' in kwargs:
            updates.append('name = ?')
            values.append(kwargs['name'])
        if 'price' in kwargs:
            updates.append('price = ?')
            values.append(kwargs['price'])
        if 'stock_status' in kwargs:
            updates.append('stock_status = ?')
            values.append(kwargs['stock_status'])
        if 'options' in kwargs:
            updates.append('options = ?')
            values.append(json.dumps(kwargs['options']) if kwargs['options'] else None)
        if 'image_path' in kwargs:
            updates.append('image_path = ?')
            values.append(kwargs['image_path'])
        
        updates.append('updated_at = ?')
        values.append(datetime.utcnow().isoformat())
        values.append(product_id)
        
        conn.execute(
            f'UPDATE products SET {", ".join(updates)} WHERE id = ?',
            values
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating product: {e}")
        return False
    finally:
        conn.close()

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db()
    try:
        row = conn.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def get_all_users():
    """Get all users"""
    conn = get_db()
    try:
        rows = conn.execute('SELECT id, username, email FROM users ORDER BY id').fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def update_user_credentials(user_id, dampfi_email, dampfi_password):
    """Update user's dampfi.ch credentials"""
    conn = get_db()
    try:
        conn.execute(
            'UPDATE users SET dampfi_email = ?, dampfi_password = ? WHERE id = ?',
            (dampfi_email, dampfi_password, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating user credentials: {e}")
        return False
    finally:
        conn.close()

def create_order(user_id, total_price, items, status='pending', confirmation_data=None):
    """Create a new order"""
    conn = get_db()
    try:
        conn.execute('''
            INSERT INTO orders (user_id, total_price, items, status, confirmation_data)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, total_price, json.dumps(items), status, json.dumps(confirmation_data) if confirmation_data else None))
        conn.commit()
        return conn.lastrowid
    except Exception as e:
        print(f"Error creating order: {e}")
        return None
    finally:
        conn.close()

def get_user_orders(user_id, limit=10):
    """Get recent orders for a user"""
    conn = get_db()
    try:
        rows = conn.execute('''
            SELECT * FROM orders 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user_id, limit)).fetchall()
        orders = []
        for row in rows:
            order = dict(row)
            if order.get('items'):
                order['items'] = json.loads(order['items'])
            if order.get('confirmation_data'):
                order['confirmation_data'] = json.loads(order['confirmation_data'])
            orders.append(order)
        return orders
    finally:
        conn.close()
