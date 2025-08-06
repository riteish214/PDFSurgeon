// PDF Tools JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    initializeFileInputs();
    initializeForms();
    initializeDragAndDrop();
});

function initializeFileInputs() {
    // Handle file input changes
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            handleFileSelection(this);
        });
    });

    // Handle conversion type changes
    const conversionType = document.getElementById('conversionType');
    if (conversionType) {
        conversionType.addEventListener('change', function() {
            updateConversionFileAccept(this.value);
        });
    }
}

function handleFileSelection(input) {
    const files = input.files;
    const formId = input.closest('form').id;
    
    if (files.length === 0) return;

    // Show file information
    if (formId === 'mergeForm') {
        displayMergeFiles(files);
    } else {
        displaySingleFile(files[0], formId);
    }
}

function displayMergeFiles(files) {
    const fileList = document.getElementById('mergeFileList');
    fileList.innerHTML = '';
    fileList.classList.remove('hidden');

    Array.from(files).forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'flex items-center justify-between p-3 bg-dark-bg border border-dark-border rounded-lg';
        fileItem.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-file-pdf text-red-500 mr-3"></i>
                <span class="text-sm font-medium">${file.name}</span>
                <span class="text-xs text-dark-secondary ml-2">(${formatFileSize(file.size)})</span>
            </div>
            <button type="button" onclick="removeFile(${index})" class="text-red-500 hover:text-red-400">
                <i class="fas fa-times"></i>
            </button>
        `;
        fileList.appendChild(fileItem);
    });
}

function displaySingleFile(file, formId) {
    const infoId = formId.replace('Form', 'FileInfo');
    const fileInfo = document.getElementById(infoId);
    
    if (fileInfo) {
        fileInfo.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-file text-neon-blue mr-3"></i>
                <div>
                    <p class="font-medium">${file.name}</p>
                    <p class="text-sm text-dark-secondary">${formatFileSize(file.size)}</p>
                </div>
            </div>
        `;
        fileInfo.classList.remove('hidden');
    }
}

function removeFile(index) {
    const input = document.getElementById('mergeFiles');
    const dt = new DataTransfer();
    
    Array.from(input.files).forEach((file, i) => {
        if (i !== index) {
            dt.items.add(file);
        }
    });
    
    input.files = dt.files;
    handleFileSelection(input);
}

function updateConversionFileAccept(conversionType) {
    const fileInput = document.getElementById('convertFile');
    
    const acceptTypes = {
        'pdf_to_docx': '.pdf',
        'pdf_to_txt': '.pdf',
        'pdf_to_csv': '.pdf',
        'docx_to_pdf': '.docx',
        'txt_to_pdf': '.txt',
        'csv_to_pdf': '.csv'
    };
    
    fileInput.accept = acceptTypes[conversionType] || '';
}

function initializeForms() {
    // Merge form
    const mergeForm = document.getElementById('mergeForm');
    if (mergeForm) {
        mergeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmit('/api/pdf/merge', new FormData(this));
        });
    }

    // Split form
    const splitForm = document.getElementById('splitForm');
    if (splitForm) {
        splitForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmit('/api/pdf/split', new FormData(this));
        });
    }

    // Compress form
    const compressForm = document.getElementById('compressForm');
    if (compressForm) {
        compressForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmit('/api/pdf/compress', new FormData(this));
        });
    }

    // Convert form
    const convertForm = document.getElementById('convertForm');
    if (convertForm) {
        convertForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmit('/api/convert', new FormData(this));
        });
    }

    // Encrypt form
    const encryptForm = document.getElementById('encryptForm');
    if (encryptForm) {
        encryptForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmit('/api/pdf/encrypt', new FormData(this));
        });
    }

    // Decrypt form
    const decryptForm = document.getElementById('decryptForm');
    if (decryptForm) {
        decryptForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmit('/api/pdf/decrypt', new FormData(this));
        });
    }
}

function handleFormSubmit(url, formData) {
    showLoadingModal();
    
    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => Promise.reject(err));
        }
        
        // Handle file download
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'download';
        
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="(.+)"/);
            if (filenameMatch) {
                filename = filenameMatch[1];
            }
        }
        
        return response.blob().then(blob => ({ blob, filename }));
    })
    .then(({ blob, filename }) => {
        hideLoadingModal();
        downloadBlob(blob, filename);
        showSuccessMessage('File processed successfully!');
    })
    .catch(error => {
        hideLoadingModal();
        console.error('Error:', error);
        showErrorMessage(error.error || 'An error occurred while processing the file.');
    });
}

function initializeDragAndDrop() {
    const dropZones = document.querySelectorAll('.file-input-custom');
    
    dropZones.forEach(zone => {
        const input = zone.querySelector('input[type="file"]') || zone.nextElementSibling?.querySelector('input[type="file"]');
        if (!input) return;

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            zone.addEventListener(eventName, preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            zone.addEventListener(eventName, () => highlight(zone), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            zone.addEventListener(eventName, () => unhighlight(zone), false);
        });

        zone.addEventListener('drop', (e) => handleDrop(e, input), false);
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
    
    input.files = files;
    handleFileSelection(input);
}

function showLoadingModal() {
    document.getElementById('loadingModal').classList.remove('hidden');
}

function hideLoadingModal() {
    document.getElementById('loadingModal').classList.add('hidden');
}

function downloadBlob(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

function showSuccessMessage(message) {
    showMessage(message, 'success');
}

function showErrorMessage(message) {
    showMessage(message, 'error');
}

function showMessage(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `fixed top-4 right-4 p-4 rounded-lg z-50 animate-fade-in ${
        type === 'success' ? 'bg-green-900 border border-green-700 text-green-100' : 'bg-red-900 border border-red-700 text-red-100'
    }`;
    
    alertDiv.innerHTML = `
        <div class="flex items-center">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} mr-2"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-gray-400 hover:text-white">
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