"""
Step 3: Setup AI Model
Downloads and configures the RealESRGAN model for realistic upscaling
"""

import os
import sys
import urllib.request
import json

# Model configuration
MODEL_INFO = {
    'name': 'RealESRGAN_x4plus',
    'url': 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth',
    'filename': 'RealESRGAN_x4plus.pth',
    'description': 'Photorealistic 4x upscaling model - high-quality image enhancement'
}

def download_file(url, destination, filename):
    """Download a file with progress reporting"""
    
    print(f"  Downloading {filename}...")
    
    try:
        def report_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, (downloaded * 100) // total_size) if total_size > 0 else 0
            mb_downloaded = downloaded / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)
            print(f'\r  Progress: {percent}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)', end='')
        
        filepath = os.path.join(destination, filename)
        urllib.request.urlretrieve(url, filepath, reporthook=report_progress)
        print()  # New line after progress
        return True
        
    except Exception as e:
        print(f"\n  ERROR downloading {filename}: {e}")
        return False

def setup_model(models_path):
    """Download and setup AI model"""
    
    # Create models directory
    os.makedirs(models_path, exist_ok=True)
    
    print(f"Model will be stored in: {models_path}")
    print()
    
    print(f"Setting up RealESRGAN model...")
    print(f"  Description: {MODEL_INFO['description']}")
    print()
    
    filepath = os.path.join(models_path, MODEL_INFO['filename'])
    
    # Check if model already exists
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath) / (1024 * 1024)
        print(f"  Model already exists ({file_size:.1f} MB)")
        print(f"  Skipping download.")
        success = True
    else:
        # Download model
        success = download_file(MODEL_INFO['url'], models_path, MODEL_INFO['filename'])
        if success:
            print(f"  ✓ Model downloaded successfully")
        else:
            print(f"  ✗ Model download failed")
    
    print()
    
    # Create model configuration file
    config = {
        'models_path': models_path,
        'presets': {
            'ultra_realistic': {
                'model_file': MODEL_INFO['filename'],
                'display_name': 'Realistic'
            }
        }
    }
    
    # Save config to Project folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(os.path.dirname(script_dir), 'Project')
    config_path = os.path.join(project_dir, 'models_config.json')
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Model configuration saved to: {config_path}")
    print()
    
    # Summary
    print("=" * 60)
    if success:
        print("Model setup completed successfully!")
        print()
        print("IMPORTANT: This model was downloaded during installation.")
        print("The application will run fully offline from now on.")
        print()
        print("Model License: BSD-3-Clause (free for commercial use)")
        print("Model Source: https://github.com/xinntao/Real-ESRGAN")
        return True
    else:
        print("Model setup failed!")
        print()
        print("You can download the model manually from:")
        print(MODEL_INFO['url'])
        print()
        print(f"Save it to: {filepath}")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        models_path = sys.argv[1]
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.join(os.path.dirname(script_dir), 'Project')
        models_path = os.path.join(project_dir, 'models')
    
    success = setup_model(models_path)
    sys.exit(0 if success else 1)
