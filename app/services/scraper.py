import requests
from bs4 import BeautifulSoup
import json
from app.config import Config
from app.database import log_message

def scrape_product_metadata(product_url):
    """
    Scrape product metadata from dampfi.ch
    Returns: dict with price, stock_status, options
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(product_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract price
        price = None
        price_selectors = [
            '.price', '.product-price', '[class*="price"]',
            '.current-price', '.special-price'
        ]
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                # Extract numeric value
                import re
                price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', '.'))
                if price_match:
                    try:
                        price = float(price_match.group().replace(',', '.'))
                        break
                    except:
                        pass
        
        # Extract product name
        name = None
        name_selectors = ['h1', '.product-name', '[class*="product-title"]']
        for selector in name_selectors:
            name_elem = soup.select_one(selector)
            if name_elem:
                name = name_elem.get_text(strip=True)
                break
        
        # Extract options (nicotine strengths) and stock status
        options = []
        stock_status = 'unknown'
        
        # Look for select dropdowns or option buttons
        option_selectors = [
            'select[name*="option"]',
            'select[name*="strength"]',
            'select[name*="nicotine"]',
            '.product-options select',
            '[class*="option"] select'
        ]
        
        for selector in option_selectors:
            select_elem = soup.select_one(selector)
            if select_elem:
                option_tags = select_elem.find_all('option')
                for opt in option_tags:
                    if opt.get('value') and opt.get('value') != '':
                        option_text = opt.get_text(strip=True)
                        # Check if option is available (not disabled, not "out of stock")
                        is_available = not opt.get('disabled') and 'out of stock' not in option_text.lower()
                        options.append({
                            'value': opt.get('value'),
                            'label': option_text,
                            'in_stock': is_available
                        })
                if options:
                    break
        
        # If no options found, try to find option buttons/links
        if not options:
            option_buttons = soup.select('[class*="option"], [data-option], [data-strength]')
            for btn in option_buttons:
                option_text = btn.get_text(strip=True)
                if option_text:
                    is_available = 'out of stock' not in option_text.lower() and 'disabled' not in btn.get('class', [])
                    options.append({
                        'value': btn.get('data-value') or btn.get('data-option') or option_text,
                        'label': option_text,
                        'in_stock': is_available
                    })
        
        # Determine overall stock status
        if options:
            in_stock_count = sum(1 for opt in options if opt.get('in_stock', False))
            if in_stock_count == 0:
                stock_status = 'out_of_stock'
            elif in_stock_count == len(options):
                stock_status = 'in_stock'
            else:
                stock_status = 'partial'
        else:
            # Try to find stock status indicators
            stock_indicators = soup.select('[class*="stock"], [class*="availability"]')
            for indicator in stock_indicators:
                text = indicator.get_text(strip=True).lower()
                if 'in stock' in text or 'available' in text:
                    stock_status = 'in_stock'
                    break
                elif 'out of stock' in text or 'unavailable' in text:
                    stock_status = 'out_of_stock'
                    break
        
        result = {
            'name': name,
            'price': price,
            'stock_status': stock_status,
            'options': options if options else None
        }
        
        log_message('info', f'Scraped product metadata', {'url': product_url, 'result': result})
        return result
        
    except requests.RequestException as e:
        log_message('error', f'Scraping failed: {str(e)}', {'url': product_url})
        return {'error': f'Failed to fetch product page: {str(e)}'}
    except Exception as e:
        log_message('error', f'Scraping error: {str(e)}', {'url': product_url})
        return {'error': f'Error parsing product page: {str(e)}'}



