/**
 * Library Management System
 * Custom JavaScript for enhanced user experience
 */

document.addEventListener('DOMContentLoaded', () => {
    // Handle alert close buttons
    const closeButtons = document.querySelectorAll('.alert .btn-close');
    closeButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const alert = button.closest('.alert');
            if (alert) {
                alert.classList.add('fade');
                setTimeout(() => {
                    alert.remove();
                }, 150);
            }
        });
    });

    // Auto-dismiss alert messages after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            } else {
                alert.classList.add('fade');
                setTimeout(() => {
                    alert.remove();
                }, 150);
            }
        }, 5000);
    });

    // Toggle password visibility in login/register forms
    const passwordTogglers = document.querySelectorAll('.password-toggle');
    passwordTogglers.forEach(toggler => {
        toggler.addEventListener('click', () => {
            const passwordField = document.querySelector(toggler.getAttribute('data-target'));
            const icon = toggler.querySelector('i');
            
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordField.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });

    // Book catalog search form - handle Enter key
    const searchForm = document.querySelector('.catalog-search-form');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="search"]');
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                searchForm.submit();
            }
        });
    }

    // Filter change in catalog
    const categorySelect = document.getElementById('category-filter');
    if (categorySelect) {
        categorySelect.addEventListener('change', () => {
            const form = categorySelect.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
    
    // Initialize tooltips (Bootstrap)
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (typeof bootstrap !== 'undefined') {
        tooltips.forEach(tooltip => {
            new bootstrap.Tooltip(tooltip);
        });
    }

    // Add animation to dashboard cards
    const cards = document.querySelectorAll('.dashboard-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.classList.add('shadow-lg');
        });
        
        card.addEventListener('mouseleave', () => {
            card.classList.remove('shadow-lg');
        });
    });

    // Confirmation for delete actions
    const confirmForms = document.querySelectorAll('form[data-confirm]');
    confirmForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const message = form.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Catalog book cover error handler
    const bookCovers = document.querySelectorAll('.book-cover');
    bookCovers.forEach(cover => {
        cover.addEventListener('error', () => {
            // Replace broken image with a placeholder
            const placeholder = document.createElement('div');
            placeholder.className = 'book-cover-placeholder d-flex align-items-center justify-content-center';
            placeholder.innerHTML = '<i class="fas fa-book fa-3x text-secondary"></i>';
            
            cover.parentNode.replaceChild(placeholder, cover);
        });
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', (event) => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        });
    });
});

// Prevent resubmission when page is refreshed
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

// Add feedback when a book is borrowed
function animateBorrowButton(button) {
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Processing...';
    setTimeout(() => {
        button.innerHTML = '<i class="fas fa-check me-1"></i> Borrowed!';
        setTimeout(() => {
            button.form.submit();
        }, 500);
    }, 800);
    return false;
}

// Add feedback when a book is returned
function animateReturnButton(button) {
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Processing...';
    setTimeout(() => {
        button.innerHTML = '<i class="fas fa-check me-1"></i> Returned!';
        setTimeout(() => {
            button.form.submit();
        }, 500);
    }, 800);
    return false;
} 