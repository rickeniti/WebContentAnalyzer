// SEO Content Analyzer JavaScript

/**
 * Copy text content to clipboard
 * @param {string} elementId - ID of the element containing text to copy
 */
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    if (!element) {
        console.error('Element not found:', elementId);
        return;
    }
    
    const text = element.textContent || element.innerText;
    
    // Use modern clipboard API if available
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('JSON copied to clipboard!', 'success');
        }).catch(err => {
            console.error('Failed to copy:', err);
            fallbackCopyTextToClipboard(text);
        });
    } else {
        fallbackCopyTextToClipboard(text);
    }
}

/**
 * Fallback method for copying text to clipboard
 * @param {string} text - Text to copy
 */
function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showToast('JSON copied to clipboard!', 'success');
    } catch (err) {
        console.error('Fallback copy failed:', err);
        showToast('Failed to copy to clipboard', 'error');
    }
    
    document.body.removeChild(textArea);
}

/**
 * Show toast notification
 * @param {string} message - Message to display
 * @param {string} type - Type of toast (success, error, info)
 */
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast align-items-center border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    // Set toast color based on type
    const colorClass = type === 'success' ? 'text-bg-success' : 
                      type === 'error' ? 'text-bg-danger' : 
                      'text-bg-info';
    toast.classList.add(colorClass);
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 3000
    });
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

/**
 * Validate form before submission
 */
function validateForm() {
    const htmlContent = document.getElementById('html_content');
    
    if (!htmlContent.value.trim()) {
        showToast('Please enter HTML content to analyze', 'error');
        htmlContent.focus();
        return false;
    }
    
    return true;
}

/**
 * Format JSON output for better readability
 */
function formatJsonOutput() {
    const jsonOutput = document.getElementById('jsonOutput');
    if (jsonOutput) {
        try {
            const jsonText = jsonOutput.textContent;
            const parsed = JSON.parse(jsonText);
            const formatted = JSON.stringify(parsed, null, 2);
            jsonOutput.textContent = formatted;
        } catch (e) {
            console.log('JSON already formatted or invalid');
        }
    }
}

/**
 * Initialize application
 */
document.addEventListener('DOMContentLoaded', function() {
    // Format JSON output if present
    formatJsonOutput();
    
    // Add form validation
    const form = document.querySelector('form[action="/analyze"]');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
            }
        });
    }
    
    // Auto-resize textarea
    const textarea = document.getElementById('html_content');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 400) + 'px';
        });
    }
    
    // Add loading state to analyze button
    const analyzeBtn = document.querySelector('button[type="submit"]');
    if (analyzeBtn) {
        const form = analyzeBtn.closest('form');
        if (form) {
            form.addEventListener('submit', function() {
                analyzeBtn.disabled = true;
                analyzeBtn.innerHTML = '<i class="bi bi-arrow-clockwise me-2"></i>Analyzing...';
            });
        }
    }
});

/**
 * API testing function for development
 */
async function testAPI() {
    const testData = {
        html: '<html><head><title>Test Page</title></head><body><h1>Test</h1><p>This is a test page with some content.</p></body></html>',
        url: 'https://example.com',
        primaryKeyword: 'test',
        relatedKeywords: ['content', 'page']
    };
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testData)
        });
        
        const result = await response.json();
        console.log('API Test Result:', result);
        return result;
    } catch (error) {
        console.error('API Test Error:', error);
        return null;
    }
}

// Make testAPI available globally for debugging
window.testAPI = testAPI;
