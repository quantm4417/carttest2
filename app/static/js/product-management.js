// Product Management
document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.getElementById('add-product-btn');
    const modal = document.getElementById('product-modal');
    const form = document.getElementById('product-form');
    const cancelBtn = document.getElementById('cancel-btn');
    const imageUpload = document.getElementById('image-upload-area');
    const fileInput = document.getElementById('product-image');
    const imagePreview = document.getElementById('image-preview');
    
    // Add product button
    addBtn?.addEventListener('click', () => {
        document.getElementById('modal-title').textContent = 'Add Product';
        document.getElementById('product-id').value = '';
        form.reset();
        imagePreview.style.display = 'none';
        modal.style.display = 'flex';
    });
    
    // Edit buttons
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const productId = btn.dataset.productId;
            await loadProductForEdit(productId);
        });
    });
    
    // Delete buttons
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const productId = btn.dataset.productId;
            if (confirm('Are you sure you want to delete this product?')) {
                await deleteProduct(productId);
            }
        });
    });
    
    // Scrape buttons
    document.querySelectorAll('.scrape-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const productId = btn.dataset.productId;
            btn.disabled = true;
            btn.textContent = 'Scraping...';
            await scrapeProduct(productId);
            btn.disabled = false;
            btn.textContent = 'Scrape Metadata';
        });
    });
    
    // Image upload
    imageUpload?.addEventListener('click', () => fileInput.click());
    imageUpload?.addEventListener('dragover', (e) => {
        e.preventDefault();
        imageUpload.style.borderColor = 'var(--primary-color)';
    });
    imageUpload?.addEventListener('dragleave', () => {
        imageUpload.style.borderColor = 'var(--border-color)';
    });
    imageUpload?.addEventListener('drop', (e) => {
        e.preventDefault();
        imageUpload.style.borderColor = 'var(--border-color)';
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleImageFile(files[0]);
        }
    });
    
    fileInput?.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleImageFile(e.target.files[0]);
        }
    });
    
    // Form submit
    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        await saveProduct();
    });
    
    cancelBtn?.addEventListener('click', () => {
        modal.style.display = 'none';
    });
});

async function loadProductForEdit(productId) {
    try {
        const response = await fetch(`/api/products/${productId}`);
        const data = await response.json();
        
        if (data.product) {
            const product = data.product;
            document.getElementById('modal-title').textContent = 'Edit Product';
            document.getElementById('product-id').value = product.id;
            document.getElementById('product-url').value = product.product_url;
            document.getElementById('product-name').value = product.name;
            
            const imagePreview = document.getElementById('image-preview');
            if (product.image_path) {
                const imageName = product.image_path.split('/').pop();
                imagePreview.src = `/uploads/${imageName}`;
                imagePreview.style.display = 'block';
            } else {
                imagePreview.style.display = 'none';
            }
            
            document.getElementById('product-modal').style.display = 'flex';
        }
    } catch (error) {
        alert('Error loading product: ' + error.message);
    }
}

async function saveProduct() {
    const productId = document.getElementById('product-id').value;
    const productUrl = document.getElementById('product-url').value.trim();
    const productName = document.getElementById('product-name').value.trim();
    const fileInput = document.getElementById('product-image');
    
    if (!productUrl || !productName) {
        alert('Please fill in all required fields');
        return;
    }
    
    try {
        let response;
        if (productId) {
            // Update
            response = await fetch(`/api/products/${productId}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    product_url: productUrl,
                    name: productName
                })
            });
        } else {
            // Create
            response = await fetch('/api/products', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    product_url: productUrl,
                    name: productName
                })
            });
        }
        
        // Check if response is JSON
        const contentType = response.headers.get('content-type');
        let data;
        
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            // Response is HTML (error page)
            const text = await response.text();
            throw new Error(`Server error (${response.status}): ${response.statusText}. Check server logs for details.`);
        }
        
        if (response.ok) {
            const savedProductId = productId || data.product.id;
            
            // Upload image if provided
            if (fileInput.files.length > 0) {
                await uploadProductImage(savedProductId, fileInput.files[0]);
            }
            
            alert('Product saved successfully!');
            window.location.reload();
        } else {
            alert('Error: ' + (data.error || 'Failed to save product'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function uploadProductImage(productId, file) {
    const formData = new FormData();
    formData.append('image', file);
    
    try {
        const response = await fetch(`/api/products/${productId}/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Upload failed');
        }
    } catch (error) {
        console.error('Image upload error:', error);
        alert('Warning: Product saved but image upload failed: ' + error.message);
    }
}

async function deleteProduct(productId) {
    try {
        const response = await fetch(`/api/products/${productId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Product deleted successfully');
            window.location.reload();
        } else {
            const data = await response.json();
            alert('Error: ' + (data.error || 'Failed to delete product'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function scrapeProduct(productId) {
    try {
        const response = await fetch(`/api/products/${productId}/scrape`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Metadata scraped successfully!');
            window.location.reload();
        } else {
            alert('Error: ' + (data.error || 'Scraping failed'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function handleImageFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = (e) => {
        const imagePreview = document.getElementById('image-preview');
        imagePreview.src = e.target.result;
        imagePreview.style.display = 'block';
    };
    reader.readAsDataURL(file);
    
    // Also set the file input
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    document.getElementById('product-image').files = dataTransfer.files;
}

