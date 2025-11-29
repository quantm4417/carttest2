from playwright.sync_api import sync_playwright
import time
from app.config import Config
from app.database import log_message
from app.models import create_order

def run_checkout(user_id, user_credentials, selected_items):
    """
    Run checkout automation using Playwright
    
    Args:
        user_id: User ID (1-5)
        user_credentials: dict with 'dampfi_email' and 'dampfi_password'
        selected_items: list of dicts with 'product_url', 'quantity', 'option_value'
    
    Returns:
        dict with 'success', 'message', 'order_data'
    """
    try:
        log_message('info', f'Starting checkout for user {user_id}', {'items_count': len(selected_items)})
        
        with sync_playwright() as p:
            # Launch browser (headless)
            browser = p.chromium.launch(headless=Config.PLAYWRIGHT_HEADLESS)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            try:
                # Step 1: Login to dampfi.ch
                log_message('info', 'Logging in to dampfi.ch')
                page.goto(f'{Config.DAMPFI_BASE_URL}/customer/account/login', wait_until='networkidle')
                
                # Fill login form
                email_input = page.locator('input[name="login[username]"], input[type="email"], #email')
                password_input = page.locator('input[name="login[password]"], input[type="password"], #pass')
                
                if email_input.count() > 0 and password_input.count() > 0:
                    email_input.fill(user_credentials['dampfi_email'])
                    password_input.fill(user_credentials['dampfi_password'])
                    
                    # Submit login
                    login_button = page.locator('button[type="submit"], button.action.login, .action.login')
                    if login_button.count() > 0:
                        login_button.click()
                        page.wait_for_timeout(2000)  # Wait for login to process
                
                # Step 2: Add all products to cart
                log_message('info', 'Adding products to cart')
                for item in selected_items:
                    product_url = item['product_url']
                    quantity = item.get('quantity', 1)
                    option_value = item.get('option_value')
                    
                    page.goto(product_url, wait_until='networkidle')
                    page.wait_for_timeout(1000)
                    
                    # Select option if provided
                    if option_value:
                        option_select = page.locator('select[name*="option"], select[name*="super_attribute"]')
                        if option_select.count() > 0:
                            option_select.select_option(option_value)
                            page.wait_for_timeout(500)
                    
                    # Set quantity
                    qty_input = page.locator('input[name="qty"], input[type="number"][name*="qty"]')
                    if qty_input.count() > 0:
                        qty_input.fill(str(quantity))
                    
                    # Click add to cart
                    add_to_cart = page.locator('button[title*="Add to Cart"], button.action.tocart, #product-addtocart-button')
                    if add_to_cart.count() > 0:
                        add_to_cart.click()
                        page.wait_for_timeout(2000)  # Wait for cart update
                
                # Step 3: Go to checkout
                log_message('info', 'Proceeding to checkout')
                page.goto(f'{Config.DAMPFI_BASE_URL}/checkout', wait_until='networkidle')
                page.wait_for_timeout(2000)
                
                # Step 4: Fill shipping information (if needed)
                # Note: Address should be saved in account, but we'll check if form appears
                shipping_form = page.locator('form[name="checkout"], #shipping-form')
                if shipping_form.count() > 0:
                    # Address should be pre-filled from account, but we can verify
                    page.wait_for_timeout(1000)
                
                # Step 5: Select payment method "Bill"
                log_message('info', 'Selecting payment method')
                bill_payment = page.locator('input[value*="bill"], input[value*="invoice"], label:has-text("Bill"), label:has-text("Rechnung")')
                if bill_payment.count() > 0:
                    bill_payment.first.click()
                    page.wait_for_timeout(1000)
                
                # Step 6: Get total price
                total_price_elem = page.locator('.grand.totals .price, .order-total .price, [class*="total"] .price')
                total_price = None
                if total_price_elem.count() > 0:
                    price_text = total_price_elem.first.inner_text()
                    import re
                    price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', '.'))
                    if price_match:
                        try:
                            total_price = float(price_match.group().replace(',', '.'))
                        except:
                            pass
                
                # Step 7: Place order
                log_message('info', 'Placing order')
                place_order_button = page.locator('button[title*="Place Order"], button.checkout, .action.primary.checkout')
                if place_order_button.count() > 0:
                    place_order_button.click()
                    page.wait_for_timeout(5000)  # Wait for order confirmation
                
                # Step 8: Get order confirmation
                confirmation_data = {}
                order_number_elem = page.locator('.order-number, [class*="order-id"], .checkout-success')
                if order_number_elem.count() > 0:
                    confirmation_data['order_number'] = order_number_elem.first.inner_text()
                
                confirmation_text = page.locator('body').inner_text()
                if 'thank you' in confirmation_text.lower() or 'bestellung' in confirmation_text.lower():
                    confirmation_data['status'] = 'confirmed'
                
                # Create order record
                order_id = create_order(
                    user_id=user_id,
                    total_price=total_price,
                    items=selected_items,
                    status='completed',
                    confirmation_data=confirmation_data
                )
                
                log_message('info', f'Checkout completed successfully', {'order_id': order_id})
                
                browser.close()
                
                return {
                    'success': True,
                    'message': 'Order placed successfully',
                    'order_id': order_id,
                    'total_price': total_price,
                    'confirmation_data': confirmation_data
                }
                
            except Exception as e:
                log_message('error', f'Checkout automation error: {str(e)}', {'user_id': user_id})
                browser.close()
                return {
                    'success': False,
                    'message': f'Checkout failed: {str(e)}',
                    'error': str(e)
                }
                
    except Exception as e:
        log_message('error', f'Playwright error: {str(e)}', {'user_id': user_id})
        return {
            'success': False,
            'message': f'Automation error: {str(e)}',
            'error': str(e)
        }



