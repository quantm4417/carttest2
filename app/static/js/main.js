// Theme Toggle
(function() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle?.querySelector('.theme-icon');
    
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    
    themeToggle?.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
    
    function updateThemeIcon(theme) {
        if (themeIcon) {
            themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }
})();

// Flash Messages Auto-hide
(function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.3s ease';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 300);
        }, 5000);
    });
})();

// Modal Close Handlers
(function() {
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('close-modal') || 
            e.target.classList.contains('modal') && e.target === e.currentTarget) {
            const modal = e.target.closest('.modal');
            if (modal) {
                modal.style.display = 'none';
            }
        }
    });
    
    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                if (modal.style.display !== 'none') {
                    modal.style.display = 'none';
                }
            });
        }
    });
})();

// Debug Mode Toggle
(function() {
    const debugToggle = document.getElementById('debug-mode');
    if (debugToggle) {
        debugToggle.addEventListener('change', (e) => {
            if (e.target.checked) {
                // Enable debug mode - could show logs panel or enable verbose logging
                console.log('Debug mode enabled');
            }
        });
    }
})();



