// Gallery Selection Management
let selection = {}; // { productId: { product, quantity, option } }

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadSelection();
    updateSelectionUI();
    
    // Add to selection buttons
    document.querySelectorAll('.add-to-selection').forEach(btn => {
        btn.addEventListener('click', handleAddToSelection);
    });
    
    // Review selection button
    const reviewBtn = document.getElementById('review-selection');
    if (reviewBtn) {
        reviewBtn.addEventListener('click', showSelectionModal);
    }
    
    // Proceed to checkout
    const proceedBtn = document.getElementById('proceed-checkout');
    if (proceedBtn) {
        proceedBtn.addEventListener('click', proceedToCheckout);
    }
    
    // Clear selection
    const clearBtn = document.getElementById('clear-selection');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearSelection);
    }
});

function handleAddToSelection(e) {
    const productId = parseInt(e.target.dataset.productId);
    const productCard = e.target.closest('.product-card');
    const productUrl = productCard.dataset.productUrl;
    
    const quantityInput = document.getElementById(`qty-${productId}`);
    const optionSelect = document.getElementById(`option-${productId}`);
    
    const quantity = parseInt(quantityInput.value) || 1;
    const optionValue = optionSelect.value;
    
    if (!optionValue) {
        alert('Please select an option first');
        return;
    }
    
    // Get product data
    const productName = productCard.querySelector('.product-name').textContent;
    const productPrice = parseFloat(productCard.querySelector('.product-price').textContent.replace(/[^\d.]/g, '')) || 0;
    const optionLabel = optionSelect.options[optionSelect.selectedIndex].text;
    
    selection[productId] = {
        product_id: productId,
        product_url: productUrl,
        product_name: productName,
        price: productPrice,
        quantity: quantity,
        option_value: optionValue,
        option_label: optionLabel
    };
    
    saveSelection();
    updateSelectionUI();
    
    // Visual feedback
    e.target.textContent = 'Added!';
    e.target.disabled = true;
    setTimeout(() => {
        e.target.textContent = 'Add to Selection';
        e.target.disabled = false;
    }, 1000);
}

function updateSelectionUI() {
    const count = Object.keys(selection).length;
    const countSpan = document.getElementById('selection-count');
    const reviewBtn = document.getElementById('review-selection');
    
    if (countSpan) countSpan.textContent = count;
    if (reviewBtn) {
        reviewBtn.disabled = count === 0;
    }
}

function showSelectionModal() {
    const modal = document.getElementById('selection-modal');
    const list = document.getElementById('selection-list');
    
    if (Object.keys(selection).length === 0) {
        alert('No items selected');
        return;
    }
    
    list.innerHTML = '';
    let total = 0;
    
    Object.values(selection).forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        const itemDiv = document.createElement('div');
        itemDiv.className = 'selection-item';
        itemDiv.innerHTML = `
            <div>
                <strong>${item.product_name}</strong>
                <p>${item.option_label} × ${item.quantity}</p>
            </div>
            <div>CHF ${itemTotal.toFixed(2)}</div>
        `;
        list.appendChild(itemDiv);
    });
    
    const totalDiv = document.createElement('div');
    totalDiv.className = 'total-section';
    totalDiv.innerHTML = `<strong>Total: CHF ${total.toFixed(2)}</strong>`;
    list.appendChild(totalDiv);
    
    modal.style.display = 'flex';
}

function proceedToCheckout() {
    const userId = parseInt(document.getElementById('user-id').value);
    if (!userId || userId < 1 || userId > 5) {
        alert('Please select a valid user (1-5)');
        return;
    }
    
    const items = Object.values(selection).map(item => ({
        product_url: item.product_url,
        quantity: item.quantity,
        option_value: item.option_value
    }));
    
    // Redirect to checkout review
    window.location.href = `/checkout/review?user_id=${userId}&items=${encodeURIComponent(JSON.stringify(items))}`;
}

function clearSelection() {
    if (confirm('Clear all selected items?')) {
        selection = {};
        saveSelection();
        updateSelectionUI();
        document.getElementById('selection-modal').style.display = 'none';
    }
}

function saveSelection() {
    localStorage.setItem('gallery_selection', JSON.stringify(selection));
}

function loadSelection() {
    const saved = localStorage.getItem('gallery_selection');
    if (saved) {
        try {
            selection = JSON.parse(saved);
        } catch (e) {
            selection = {};
        }
    }
}

// Load selection from URL params (when coming from gallery)
const urlParams = new URLSearchParams(window.location.search);
const itemsParam = urlParams.get('items');
if (itemsParam) {
    try {
        const items = JSON.parse(decodeURIComponent(itemsParam));
        // Store in session for checkout
        sessionStorage.setItem('checkout_items', JSON.stringify(items));
        sessionStorage.setItem('checkout_user_id', urlParams.get('user_id'));
    } catch (e) {
        console.error('Error parsing items from URL:', e);
    }
}



