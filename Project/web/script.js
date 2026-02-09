// Global state
let selectedFile = null;
let selectedMode = 'factor'; // 'factor' or 'resolution'
let selectedScaleFactor = null;
let targetWidth = null;
let targetHeight = null;
let scaleFactors = [];

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('previewContainer');
const imagePreview = document.getElementById('imagePreview');
const removeBtn = document.getElementById('removeBtn');
const modeSection = document.getElementById('modeSection');
const modeFactorCard = document.getElementById('modeFactorCard');
const modeResolutionCard = document.getElementById('modeResolutionCard');
const scaleSection = document.getElementById('scaleSection');
const scaleGrid = document.getElementById('scaleGrid');
const resolutionSection = document.getElementById('resolutionSection');
const widthInput = document.getElementById('widthInput');
const heightInput = document.getElementById('heightInput');
const actionSection = document.getElementById('actionSection');
const upscaleBtn = document.getElementById('upscaleBtn');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');
const resultSection = document.getElementById('resultSection');
const resultImage = document.getElementById('resultImage');
const downloadBtn = document.getElementById('downloadBtn');
const newUpscaleBtn = document.getElementById('newUpscaleBtn');
const statusMessage = document.getElementById('statusMessage');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadScaleFactors();
    setupEventListeners();
});

// Load available scale factors from API
async function loadScaleFactors() {
    try {
        const response = await fetch('/api/scale-factors');
        const data = await response.json();
        
        if (data.scale_factors) {
            scaleFactors = data.scale_factors;
            renderScaleFactors();
        } else {
            showStatus('Failed to load scale factors', 'error');
        }
    } catch (error) {
        showStatus('Error loading scale factors: ' + error.message, 'error');
    }
}

// Render scale factor cards
function renderScaleFactors() {
    scaleGrid.innerHTML = '';
    
    scaleFactors.forEach(factor => {
        const card = document.createElement('div');
        card.className = 'scale-card';
        card.dataset.scaleFactor = factor;
        card.innerHTML = `
            <div class="scale-number">${factor}×</div>
            <div class="scale-label">larger</div>
        `;
        
        card.addEventListener('click', () => selectScaleFactor(factor));
        scaleGrid.appendChild(card);
    });
}

// Setup event listeners
function setupEventListeners() {
    // Upload area click
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });
    
    // Remove button
    removeBtn.addEventListener('click', resetUpload);
    
    // Mode selection
    modeFactorCard.addEventListener('click', () => selectMode('factor'));
    modeResolutionCard.addEventListener('click', () => selectMode('resolution'));
    
    // Resolution inputs
    widthInput.addEventListener('input', updateResolution);
    heightInput.addEventListener('input', updateResolution);
    
    // Resolution preset buttons
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            widthInput.value = btn.dataset.width;
            heightInput.value = btn.dataset.height;
            updateResolution();
        });
    });
    
    // Upscale button
    upscaleBtn.addEventListener('click', handleUpscale);
    
    // Download button
    downloadBtn.addEventListener('click', handleDownload);
    
    // New upscale button
    newUpscaleBtn.addEventListener('click', resetAll);
}

// Handle file selection
function handleFileSelect(file) {
    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp', 'image/bmp'];
    if (!validTypes.includes(file.type)) {
        showStatus('Invalid file type. Please upload PNG, JPG, JPEG, WEBP, or BMP.', 'error');
        return;
    }
    
    // Validate file size (50MB)
    if (file.size > 50 * 1024 * 1024) {
        showStatus('File too large. Maximum size is 50MB.', 'error');
        return;
    }
    
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        uploadArea.style.display = 'none';
        previewContainer.style.display = 'block';
        modeSection.style.display = 'block';
        actionSection.style.display = 'block';
        
        // Show the appropriate section based on mode
        if (selectedMode === 'factor') {
            scaleSection.style.display = 'block';
            resolutionSection.style.display = 'none';
        } else {
            scaleSection.style.display = 'none';
            resolutionSection.style.display = 'block';
        }
        
        updateUpscaleButton();
    };
    reader.readAsDataURL(file);
}

// Select mode
function selectMode(mode) {
    selectedMode = mode;
    
    // Update UI
    if (mode === 'factor') {
        modeFactorCard.classList.add('selected');
        modeResolutionCard.classList.remove('selected');
        scaleSection.style.display = 'block';
        resolutionSection.style.display = 'none';
        
        // Clear resolution inputs
        targetWidth = null;
        targetHeight = null;
    } else {
        modeFactorCard.classList.remove('selected');
        modeResolutionCard.classList.add('selected');
        scaleSection.style.display = 'none';
        resolutionSection.style.display = 'block';
        
        // Clear scale factor selection
        selectedScaleFactor = null;
        document.querySelectorAll('.scale-card').forEach(card => {
            card.classList.remove('selected');
        });
    }
    
    updateUpscaleButton();
}

// Select scale factor
function selectScaleFactor(factor) {
    selectedScaleFactor = factor;
    
    // Update UI
    document.querySelectorAll('.scale-card').forEach(card => {
        if (parseInt(card.dataset.scaleFactor) === factor) {
            card.classList.add('selected');
        } else {
            card.classList.remove('selected');
        }
    });
    
    updateUpscaleButton();
}

// Update resolution from inputs
function updateResolution() {
    const width = parseInt(widthInput.value);
    const height = parseInt(heightInput.value);
    
    if (width > 0 && height > 0) {
        targetWidth = width;
        targetHeight = height;
    } else {
        targetWidth = null;
        targetHeight = null;
    }
    
    updateUpscaleButton();
}

// Update upscale button state
function updateUpscaleButton() {
    if (!selectedFile) {
        upscaleBtn.disabled = true;
        return;
    }
    
    if (selectedMode === 'factor') {
        upscaleBtn.disabled = !selectedScaleFactor;
    } else {
        upscaleBtn.disabled = !(targetWidth && targetHeight);
    }
}

// Handle upscale
async function handleUpscale() {
    if (!selectedFile) {
        return;
    }
    
    if (selectedMode === 'factor' && !selectedScaleFactor) {
        return;
    }
    
    if (selectedMode === 'resolution' && (!targetWidth || !targetHeight)) {
        return;
    }
    
    // Disable button and show loading
    upscaleBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-flex';
    
    let statusMsg = '';
    if (selectedMode === 'factor') {
        statusMsg = `Upscaling your image ${selectedScaleFactor}x... This may take a few moments.`;
    } else {
        statusMsg = `Upscaling your image to ${targetWidth}×${targetHeight}... This may take a few moments.`;
    }
    showStatus(statusMsg, 'info');
    
    try {
        // Create form data
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('mode', selectedMode);
        
        if (selectedMode === 'factor') {
            formData.append('scale_factor', selectedScaleFactor);
        } else {
            formData.append('target_width', targetWidth);
            formData.append('target_height', targetHeight);
        }
        
        // Upload and process
        const response = await fetch('/api/upscale', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Show result
            showResult(data.output_file, data);
            showStatus(data.message + ` (${data.original_size} → ${data.upscaled_size})`, 'success');
        } else {
            throw new Error(data.error || 'Upscaling failed');
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        upscaleBtn.disabled = false;
    }
}

// Show result
function showResult(filename, data) {
    // Hide upload and processing sections
    previewContainer.style.display = 'none';
    modeSection.style.display = 'none';
    scaleSection.style.display = 'none';
    resolutionSection.style.display = 'none';
    actionSection.style.display = 'none';
    
    // Show result
    resultImage.src = '/api/download/' + filename;
    resultImage.dataset.filename = filename;
    resultSection.style.display = 'block';
    
    // Reset button
    btnText.style.display = 'inline';
    btnLoader.style.display = 'none';
    upscaleBtn.disabled = false;
}

// Handle download
function handleDownload() {
    const filename = resultImage.dataset.filename;
    if (filename) {
        window.location.href = '/api/download/' + filename;
    }
}

// Reset upload
function resetUpload() {
    selectedFile = null;
    selectedScaleFactor = null;
    targetWidth = null;
    targetHeight = null;
    fileInput.value = '';
    widthInput.value = '';
    heightInput.value = '';
    uploadArea.style.display = 'block';
    previewContainer.style.display = 'none';
    modeSection.style.display = 'none';
    scaleSection.style.display = 'none';
    resolutionSection.style.display = 'none';
    actionSection.style.display = 'none';
    hideStatus();
}

// Reset all
function resetAll() {
    selectedFile = null;
    selectedMode = 'factor';
    selectedScaleFactor = null;
    targetWidth = null;
    targetHeight = null;
    fileInput.value = '';
    widthInput.value = '';
    heightInput.value = '';
    
    // Reset UI
    uploadArea.style.display = 'block';
    previewContainer.style.display = 'none';
    modeSection.style.display = 'none';
    scaleSection.style.display = 'none';
    resolutionSection.style.display = 'none';
    actionSection.style.display = 'none';
    resultSection.style.display = 'none';
    
    // Clear selections
    modeFactorCard.classList.add('selected');
    modeResolutionCard.classList.remove('selected');
    document.querySelectorAll('.scale-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    updateUpscaleButton();
    hideStatus();
}

// Show status message
function showStatus(message, type = 'info') {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.style.display = 'block';
}

// Hide status message
function hideStatus() {
    statusMessage.style.display = 'none';
}
