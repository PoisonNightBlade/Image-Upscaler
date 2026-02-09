"""
Backend Server for Offline AI Image Upscaler
Handles image upload, processing, and serving the web UI
"""

import os
import sys
import json
import webbrowser
from threading import Timer
from flask import Flask, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import cv2
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
SCALE_FACTORS = [2, 3, 5, 10]  # Available scaling multipliers
PRESET = 'ultra_realistic'  # Fixed preset - realistic upscaling only

# Create Flask app
app = Flask(__name__, static_folder='web', static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Global upscaler cache
upscalers = {}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_models_config():
    """Load models configuration"""
    try:
        with open('models_config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading models configuration: {e}")
        return None

def initialize_upscaler(config):
    """Initialize RealESRGAN upscaler for realistic upscaling"""
    
    if PRESET in upscalers:
        return upscalers[PRESET]
    
    try:
        preset_config = config['presets'][PRESET]
        model_path = os.path.join(config['models_path'], preset_config['model_file'])
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # RealESRGAN_x4plus - Full RRDB network for photorealistic enhancement
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        
        # Initialize upscaler with GPU/CPU auto-detection
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        upscaler = RealESRGANer(
            scale=netscale,
            model_path=model_path,
            model=model,
            tile=400 if device == 'cuda' else 200,  # Smaller tiles for CPU
            tile_pad=10,
            pre_pad=0,
            half=torch.cuda.is_available(),  # Use FP16 on GPU for speed
            device=device
        )
        
        upscalers[PRESET] = upscaler
        print(f"✓ Initialized upscaler on {device.upper()}")
        return upscaler
        
    except Exception as e:
        print(f"ERROR initializing upscaler: {e}")
        import traceback
        traceback.print_exc()
        return None

def upscale_with_factor(image_path, scale_factor, config):
    """Upscale image by a specific factor
    
    Args:
        image_path: Path to input image
        scale_factor: Multiplier (2, 3, 5, or 10)
        config: Models configuration
    
    Returns:
        Upscaled image as numpy array
    """
    
    try:
        # Load image
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Failed to load image")
        
        original_height, original_width = img.shape[:2]
        print(f"Original image size: {original_width}x{original_height}")
        
        # Initialize upscaler
        upscaler = initialize_upscaler(config)
        if upscaler is None:
            raise ValueError(f"Failed to initialize upscaler")
        
        # Calculate target dimensions
        target_width = original_width * scale_factor
        target_height = original_height * scale_factor
        
        print(f"Upscaling {scale_factor}x...")
        print(f"Target size: {target_width}x{target_height}")
        
        # The models natively upscale 4x, so we need to handle different scale factors
        if scale_factor == 2:
            # Upscale 4x then downscale to 2x
            output, _ = upscaler.enhance(img, outscale=4)
            output = cv2.resize(output, (target_width, target_height), interpolation=cv2.INTER_AREA)
        elif scale_factor == 3:
            # Upscale 4x then downscale to 3x
            output, _ = upscaler.enhance(img, outscale=4)
            output = cv2.resize(output, (target_width, target_height), interpolation=cv2.INTER_AREA)
        elif scale_factor == 5:
            # Upscale 4x, then upscale again by 1.25x
            output, _ = upscaler.enhance(img, outscale=4)
            output = cv2.resize(output, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
        elif scale_factor == 10:
            # Upscale 4x twice (but limit to avoid memory issues)
            # First pass: 4x
            output, _ = upscaler.enhance(img, outscale=4)
            # Second pass: resize to 10x total (2.5x from current size)
            output = cv2.resize(output, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
        else:
            # Default: use outscale parameter directly if supported
            output, _ = upscaler.enhance(img, outscale=scale_factor)
        
        final_height, final_width = output.shape[:2]
        print(f"Final upscaled size: {final_width}x{final_height}")
        
        return output
        
    except Exception as e:
        print(f"ERROR during upscaling: {e}")
        import traceback
        traceback.print_exc()
        raise

def upscale_to_resolution(image_path, target_width, target_height, config):
    """Upscale image to specific resolution without stretching
    
    Uses intelligent upscaling to reach target resolution without distortion.
    Maintains aspect ratio by cropping or padding if needed.
    
    Args:
        image_path: Path to input image
        target_width: Desired width in pixels
        target_height: Desired height in pixels
        config: Models configuration
    
    Returns:
        Upscaled image as numpy array
    """
    
    try:
        # Load image
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Failed to load image")
        
        original_height, original_width = img.shape[:2]
        print(f"Original image size: {original_width}x{original_height}")
        print(f"Target resolution: {target_width}x{target_height}")
        
        # Calculate aspect ratios
        original_aspect = original_width / original_height
        target_aspect = target_width / target_height
        
        # Initialize upscaler
        upscaler = initialize_upscaler(config)
        if upscaler is None:
            raise ValueError(f"Failed to initialize upscaler")
        
        # Calculate the scale factor needed to reach or exceed the target resolution
        # while maintaining aspect ratio
        scale_w = target_width / original_width
        scale_h = target_height / original_height
        
        # Use the larger scale to ensure we meet both dimensions
        needed_scale = max(scale_w, scale_h)
        
        # Round up to ensure we have enough pixels
        import math
        needed_scale = math.ceil(needed_scale)
        
        # Clamp to reasonable values
        needed_scale = max(2, min(needed_scale, 10))
        
        print(f"Using {needed_scale}x upscale to reach target resolution")
        
        # Upscale using the calculated factor
        if needed_scale == 4:
            # Native 4x upscale
            output, _ = upscaler.enhance(img, outscale=4)
        elif needed_scale == 2:
            # Upscale 4x then downscale to 2x
            output, _ = upscaler.enhance(img, outscale=4)
            temp_width = original_width * 2
            temp_height = original_height * 2
            output = cv2.resize(output, (temp_width, temp_height), interpolation=cv2.INTER_AREA)
        elif needed_scale == 3:
            # Upscale 4x then downscale to 3x
            output, _ = upscaler.enhance(img, outscale=4)
            temp_width = original_width * 3
            temp_height = original_height * 3
            output = cv2.resize(output, (temp_width, temp_height), interpolation=cv2.INTER_AREA)
        else:
            # For scales >= 5, upscale 4x then resize
            output, _ = upscaler.enhance(img, outscale=4)
            temp_width = original_width * needed_scale
            temp_height = original_height * needed_scale
            output = cv2.resize(output, (temp_width, temp_height), interpolation=cv2.INTER_CUBIC)
        
        current_height, current_width = output.shape[:2]
        print(f"After AI upscale: {current_width}x{current_height}")
        
        # Now intelligently crop or pad to exact target resolution
        # Calculate center crop if aspect ratios differ
        if abs(original_aspect - target_aspect) > 0.01:
            # Aspect ratios differ - we need to crop
            current_aspect = current_width / current_height
            
            if current_aspect > target_aspect:
                # Image is wider - crop width
                new_width = int(current_height * target_aspect)
                start_x = (current_width - new_width) // 2
                output = output[:, start_x:start_x + new_width]
            else:
                # Image is taller - crop height
                new_height = int(current_width / target_aspect)
                start_y = (current_height - new_height) // 2
                output = output[start_y:start_y + new_height, :]
            
            current_height, current_width = output.shape[:2]
            print(f"After aspect ratio adjustment: {current_width}x{current_height}")
        
        # Final resize to exact target resolution (should be minimal quality loss)
        if current_width != target_width or current_height != target_height:
            # Use high-quality Lanczos interpolation for final adjustment
            output = cv2.resize(output, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)
        
        final_height, final_width = output.shape[:2]
        print(f"Final resolution: {final_width}x{final_height}")
        
        return output
        
    except Exception as e:
        print(f"ERROR during upscaling: {e}")
        import traceback
        traceback.print_exc()
        raise

@app.route('/')
def index():
    """Serve the main web UI"""
    return send_from_directory('web', 'index.html')

@app.route('/api/scale-factors')
def get_scale_factors():
    """Get available scale factors"""
    return jsonify({'scale_factors': SCALE_FACTORS})

@app.route('/api/upscale', methods=['POST'])
def upscale():
    """Handle image upload and upscaling"""
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, WEBP, BMP'}), 400
    
    # Get upscale mode (factor or resolution)
    upscale_mode = request.form.get('mode', 'factor')
    
    # Load configuration
    config = load_models_config()
    if not config:
        return jsonify({'error': 'Failed to load configuration'}), 500
    
    try:
        # Save uploaded file
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Get original dimensions
        original_img = cv2.imread(input_path)
        orig_h, orig_w = original_img.shape[:2]
        
        # Process based on mode
        if upscale_mode == 'factor':
            # Scale factor mode
            try:
                scale_factor = int(request.form.get('scale_factor', 2))
                if scale_factor not in SCALE_FACTORS:
                    return jsonify({'error': f'Invalid scale factor. Must be one of: {SCALE_FACTORS}'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid scale factor'}), 400
            
            # Upscale image
            output_img = upscale_with_factor(input_path, scale_factor, config)
            output_filename = f"upscaled_{scale_factor}x_{filename}"
            
        elif upscale_mode == 'resolution':
            # Target resolution mode
            try:
                target_width = int(request.form.get('target_width'))
                target_height = int(request.form.get('target_height'))
                
                if target_width <= 0 or target_height <= 0:
                    return jsonify({'error': 'Invalid target resolution'}), 400
                
                if target_width > 20000 or target_height > 20000:
                    return jsonify({'error': 'Target resolution too large (max 20000px)'}), 400
                    
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid target resolution'}), 400
            
            # Upscale to target resolution
            output_img = upscale_to_resolution(input_path, target_width, target_height, config)
            output_filename = f"upscaled_{target_width}x{target_height}_{filename}"
            
        else:
            return jsonify({'error': 'Invalid upscale mode'}), 400
        
        # Save output
        os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        cv2.imwrite(output_path, output_img)
        
        final_h, final_w = output_img.shape[:2]
        
        # Clean up input file
        os.remove(input_path)
        
        return jsonify({
            'success': True,
            'output_file': output_filename,
            'message': f'Image upscaled successfully',
            'original_size': f'{orig_w}x{orig_h}',
            'upscaled_size': f'{final_w}x{final_h}'
        })
        
    except Exception as e:
        print(f"ERROR processing image: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download(filename):
    """Download upscaled image"""
    try:
        return send_file(
            os.path.join(app.config['OUTPUT_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

def open_browser():
    """Open web browser after a short delay"""
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Load and verify configuration
    config = load_models_config()
    if not config:
        print("ERROR: Could not load models configuration!")
        print("Please run install.bat first.")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("AI Image Upscaler - Offline & Private")
    print("="*60)
    print(f"\nDevice: {'CUDA (GPU)' if torch.cuda.is_available() else 'CPU'}")
    print(f"Models path: {config['models_path']}")
    print(f"\nUpscaling method: Realistic (High Quality)")
    print("\n" + "="*60)
    print("\nStarting server on http://localhost:5000")
    print("Opening web browser...")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Open browser after 1.5 seconds
    Timer(1.5, open_browser).start()
    
    # Start Flask server
    app.run(host='localhost', port=5000, debug=False)
