// File Sharing JavaScript functionality

document.addEventListener('DOMContentLoaded', function () {
    initializeShareForms();
    initializeAccessForm();
    initializeDragAndDrop();
});

function initializeShareForms() {
    // File share form
    const fileShareForm = document.getElementById('fileShareForm');
    if (fileShareForm) {
        fileShareForm.addEventListener('submit', function (e) {
            e.preventDefault();
            handleFileShare(new FormData(this));
        });
    }

    // File input change handler
    const fileInput = document.getElementById('shareFile');
    if (fileInput) {
        fileInput.addEventListener('change', function () {
            displayFileInfo(this.files[0]);
        });
    }
}

function initializeAccessForm() {
    const accessForm = document.getElementById('accessForm');
    if (accessForm) {
        accessForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const accessCode = document.getElementById('accessCodeInput').value.trim().toUpperCase();
            if (accessCode) {
                window.open(`/shared/${accessCode}`, '_blank');
            }
        });
    }

    // Auto-format access code input
    const accessCodeInput = document.getElementById('accessCodeInput');
    if (accessCodeInput) {
        accessCodeInput.addEventListener('input', function () {
            this.value = this.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
        });
    }
}

function displayFileInfo(file) {
    if (!file) return;

    const fileInfo = document.getElementById('fileInfo');
    fileInfo.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-file text-neon-blue mr-3"></i>
            <div>
                <p class="font-medium">${file.name}</p>
                <p class="text-sm text-dark-secondary">${formatFileSize(file.size)} - ${file.type}</p>
            </div>
        </div>
    `;
    fileInfo.classList.remove('hidden');
}

function handleFileShare(formData) {
    const fileInput = document.getElementById('shareFile');
    if (!fileInput.files[0]) {
        showErrorMessage('Please select a file to share.');
        return;
    }

    showLoadingModal();

    fetch('/api/share/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            hideLoadingModal();
            if (data.success) {
                displayShareResult(data);
                resetForm('fileShareForm');
            } else {
                showErrorMessage(data.error || 'Failed to share file.');
            }
        })
        .catch(error => {
            hideLoadingModal();
            console.error('Error:', error);
            showErrorMessage('An error occurred while sharing the file.');
        });
}

function displayShareResult(data) {
    const shareResult = document.getElementById('shareResult');
    shareResult.classList.remove('hidden');

    document.getElementById('accessCode').value = data.access_code;
    document.getElementById('shareUrl').value = data.share_url;

    const qrCode = document.getElementById('qrCode');
    qrCode.src = data.qr_code_url;

    if (data.expires_at) {
        const expiryDate = new Date(data.expires_at);
        document.getElementById('expiryTime').textContent = expiryDate.toLocaleString();
    }

    shareResult.scrollIntoView({ behavior: 'smooth' });

    showSuccessMessage('File shared successfully! Share the access code or QR code.');
}

function resetForm(formId) {
    const form = document.getElementById(formId);
    form.reset();

    const fileInfo = document.getElementById('fileInfo');
    if (fileInfo) {
        fileInfo.classList.add('hidden');
    }
}

function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    element.select();
    element.setSelectionRange(0, 99999);

    try {
        document.execCommand('copy');
        showSuccessMessage('Copied to clipboard!');
    } catch (err) {
        navigator.clipboard.writeText(element.value).then(() => {
            showSuccessMessage('Copied to clipboard!');
        }).catch(() => {
            showErrorMessage('Failed to copy to clipboard.');
        });
    }
}

function initializeDragAndDrop() {
    const dropZone = document.querySelector('.file-input-custom');
    const fileInput = document.getElementById('shareFile');

    if (!dropZone || !fileInput) return;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => highlight(dropZone), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => unhighlight(dropZone), false);
    });

    dropZone.addEventListener('drop', (e) => handleDrop(e, fileInput), false);
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
        displayFileInfo(files[0]);
    }
}

function showLoadingModal() {
    document.getElementById('loadingModal').classList.remove('hidden');
}

function hideLoadingModal() {
    document.getElementById('loadingModal').classList.add('hidden');
}

function showSuccessMessage(message) {
    showMessage(message, 'success');
}

function showErrorMessage(message) {
    showMessage(message, 'error');
}

function showMessage(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `fixed top-4 right-4 p-4 rounded-lg z-50 animate-fade-in max-w-sm ${
        type === 'success' ? 'bg-green-900 border border-green-700 text-green-100' : 'bg-red-900 border border-red-700 text-red-100'
    }`;

    alertDiv.innerHTML = `
        <div class="flex items-center">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} mr-2"></i>
            <span class="flex-1">${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-gray-400 hover:text-white">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    document.body.appendChild(alertDiv);

    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
