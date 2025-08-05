// Main JavaScript file for PDF Tools application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize file input enhancements
    initializeFileInputs();
    
    // Initialize form validations
    initializeFormValidations();
    
    // Initialize drag and drop
    initializeDragAndDrop();
    
    // Initialize loading states
    initializeLoadingStates();
});

/**
 * Enhance file input elements with better UX
 */
function initializeFileInputs() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        // Add change event listener for file size validation
        input.addEventListener('change', function(e) {
            validateFileSize(e.target);
        });
    });
}

/**
 * Validate file size against maximum allowed
 */
function validateFileSize(input) {
    const maxSize = 100 * 1024 * 1024; // 100MB
    const files = input.files;
    
    for (let file of files) {
        if (file.size > maxSize) {
            showAlert(`File "${file.name}" is too large. Maximum size is 100MB.`, 'danger');
            input.value = ''; // Clear the input
            return false;
        }
    }
    return true;
}

/**
 * Initialize form validations
 */
function initializeFormValidations() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
                return false;
            }
            
            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                setLoadingState(submitBtn, true);
            }
        });
    });
}

/**
 * Validate form before submission
 */
function validateForm(form) {
    const fileInputs = form.querySelectorAll('input[type="file"]');
    
    // Check if files are selected
    for (let input of fileInputs) {
        if (input.required && input.files.length === 0) {
            showAlert('Please select a file.', 'danger');
            return false;
        }
        
        // Validate file size
        if (!validateFileSize(input)) {
            return false;
        }
    }
    
    // Check password field if present
    const passwordInput = form.querySelector('input[type="password"]');
    if (passwordInput && passwordInput.required && passwordInput.value.length < 8) {
        showAlert('Password must be at least 8 characters long.', 'danger');
        return false;
    }
    
    return true;
}

/**
 * Initialize drag and drop functionality
 */
function initializeDragAndDrop() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        const container = input.closest('.card-body') || input.parentElement;
        
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            container.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });
        
        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            container.addEventListener(eventName, () => highlight(container), false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            container.addEventListener(eventName, () => unhighlight(container), false);
        });
        
        // Handle dropped files
        container.addEventListener('drop', (e) => handleDrop(e, input), false);
    });
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(element) {
    element.classList.add('dragover');
}

function unhighlight(element) {
    element.classList.remove('dragover');
}

function handleDrop(e, input) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        input.files = files;
        
        // Trigger change event
        const changeEvent = new Event('change', { bubbles: true });
        input.dispatchEvent(changeEvent);
    }
}

/**
 * Initialize loading states for forms
 */
function initializeLoadingStates() {
    // Reset loading states on page load
    const loadingButtons = document.querySelectorAll('.btn.loading');
    loadingButtons.forEach(btn => {
        setLoadingState(btn, false);
    });
}

/**
 * Set loading state for a button
 */
function setLoadingState(button, isLoading) {
    if (isLoading) {
        button.classList.add('loading');
        button.disabled = true;
        button.setAttribute('data-original-text', button.textContent);
        button.textContent = 'Processing...';
    } else {
        button.classList.remove('loading');
        button.disabled = false;
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.textContent = originalText;
            button.removeAttribute('data-original-text');
        }
    }
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert after navbar
    const navbar = document.querySelector('.navbar');
    if (navbar && navbar.nextSibling) {
        navbar.parentNode.insertBefore(alert, navbar.nextSibling);
    } else {
        alertContainer.insertBefore(alert, alertContainer.firstChild);
    }
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Generate unique filename with timestamp
 */
function generateUniqueFilename(originalName, suffix = '') {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const name = originalName.substring(0, originalName.lastIndexOf('.'));
    const ext = originalName.substring(originalName.lastIndexOf('.'));
    
    return `${name}${suffix}_${timestamp}${ext}`;
}

/**
 * Smooth scroll to element
 */
function scrollToElement(element) {
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Export functions for use in other scripts
window.PDFTools = {
    showAlert,
    setLoadingState,
    formatFileSize,
    generateUniqueFilename,
    scrollToElement
};
