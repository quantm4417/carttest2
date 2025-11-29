// Checkout Review and Confirmation
document.addEventListener('DOMContentLoaded', () => {
    loadCheckoutData();
    
    const confirmBtn = document.getElementById('confirm-checkout-btn');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', handleCheckout);
    }
});

async function loadCheckoutData() {
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('user_id');
    const itemsParam = urlParams.get('items');
    
    if (!itemsParam) {
        // Try to load from session storage
        const savedItems = sessionStorage.getItem('checkout_items');
        const savedUserId = sessionStorage.getItem('checkout_user_id');
        
        if (!savedItems || !savedUserId) {
            alert('No items selected. Redirecting to gallery...');
            window.location.href = '/';
            return;
        }
        
        displayCheckoutSummary(JSON.parse(savedItems), savedUserId);
        return;
    }
    
    try {
        const items = JSON.parse(decodeURIComponent(itemsParam));
        displayCheckoutSummary(items, userId);
        
        // Save to session
        sessionStorage.setItem('checkout_items', JSON.stringify(items));
        sessionStorage.setItem('checkout_user_id', userId);
    } catch (e) {
        console.error('Error parsing checkout data:', e);
        alert('Error loading checkout data');
        window.location.href = '/';
    }
}

async function displayCheckoutSummary(items, userId) {
    const summaryDiv = document.getElementById('items-summary');
    let total = 0;
    
    // Fetch product details for display
    const itemsWithDetails = await Promise.all(items.map(async (item) => {
        try {
            // Try to get product details from products list
            const response = await fetch('/api/products');
            const data = await response.json();
            const product = data.products.find(p => p.product_url === item.product_url);
            
            return {
                ...item,
                product_name: product?.name || 'Unknown Product',
                price: product?.price || 0
            };
        } catch (e) {
            return {
                ...item,
                product_name: 'Unknown Product',
                price: 0
            };
        }
    }));
    
    summaryDiv.innerHTML = '';
    
    itemsWithDetails.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        const itemDiv = document.createElement('div');
        itemDiv.className = 'checkout-item';
        itemDiv.style.cssText = 'padding: 1rem; margin-bottom: 1rem; background: var(--input-bg); border-radius: var(--border-radius);';
        itemDiv.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <strong>${item.product_name}</strong>
                    <p style="margin-top: 0.5rem; color: var(--text-secondary); font-size: 0.9rem;">
                        Option: ${item.option_value || 'N/A'} × ${item.quantity}
                    </p>
                </div>
                <div style="font-weight: 600;">CHF ${itemTotal.toFixed(2)}</div>
            </div>
        `;
        summaryDiv.appendChild(itemDiv);
    });
    
    document.getElementById('total-price').textContent = `CHF ${total.toFixed(2)}`;
}

async function handleCheckout() {
    const confirmBtn = document.getElementById('confirm-checkout-btn');
    const progressModal = document.getElementById('checkout-progress-modal');
    const progressMessage = document.getElementById('progress-message');
    
    if (!confirm('Are you sure you want to place this order? This will proceed with checkout on dampfi.ch')) {
        return;
    }
    
    // Get checkout data
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('user_id');
    const itemsParam = urlParams.get('items');
    
    let items;
    try {
        items = itemsParam ? JSON.parse(decodeURIComponent(itemsParam)) : JSON.parse(sessionStorage.getItem('checkout_items'));
    } catch (e) {
        alert('Error: Invalid checkout data');
        return;
    }
    
    // Show progress modal
    progressModal.style.display = 'flex';
    confirmBtn.disabled = true;
    progressMessage.textContent = 'Adding items to cart...';
    
    try {
        const response = await fetch('/api/checkout/confirm', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                user_id: parseInt(userId),
                items: items
            })
        });
        
        const data = await response.json();
        
        progressModal.style.display = 'none';
        
        if (data.success) {
            alert(`Order placed successfully!\n\nTotal: CHF ${data.total_price?.toFixed(2) || 'N/A'}\n${data.confirmation_data?.order_number ? 'Order #: ' + data.confirmation_data.order_number : ''}`);
            
            // Clear session storage
            sessionStorage.removeItem('checkout_items');
            sessionStorage.removeItem('checkout_user_id');
            
            // Redirect to gallery
            window.location.href = '/';
        } else {
            alert('Checkout failed: ' + (data.message || data.error || 'Unknown error'));
            confirmBtn.disabled = false;
        }
    } catch (error) {
        progressModal.style.display = 'none';
        alert('Error: ' + error.message);
        confirmBtn.disabled = false;
    }
}



