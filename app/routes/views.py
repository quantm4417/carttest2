from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from app.models import get_all_products, get_product_by_id, get_user_by_id, get_user_orders
from app.database import log_message
from app.config import Config
import os

bp = Blueprint('views', __name__)

@bp.route('/')
def gallery():
    """Main gallery view"""
    products = get_all_products()
    return render_template('gallery.html', products=products)

@bp.route('/product-management')
def product_management():
    """Product management view"""
    products = get_all_products()
    return render_template('product_management.html', products=products)

@bp.route('/checkout/review')
def checkout_review():
    """Review selection before checkout"""
    user_id = request.args.get('user_id', type=int)
    if not user_id or not (1 <= user_id <= 5):
        flash('Please select a valid user (1-5)', 'error')
        return redirect(url_for('views.gallery'))
    
    user = get_user_by_id(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('views.gallery'))
    
    if not user.get('dampfi_email'):
        flash('User credentials not set up. Please configure user credentials first.', 'error')
        return redirect(url_for('views.user_setup', user_id=user_id))
    
    # Get recent orders for reporting
    recent_orders = get_user_orders(user_id, limit=5)
    
    return render_template('checkout_review.html', user=user, recent_orders=recent_orders)

@bp.route('/user/setup')
def user_setup():
    """User credentials setup page"""
    user_id = request.args.get('user_id', type=int)
    if not user_id or not (1 <= user_id <= 5):
        flash('Invalid user ID', 'error')
        return redirect(url_for('views.gallery'))
    
    user = get_user_by_id(user_id)
    return render_template('user_setup.html', user=user, user_id=user_id)

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded product images"""
    return send_from_directory(Config.UPLOAD_FOLDER, filename)

