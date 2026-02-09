"""
Step 2: Install Dependencies
Installs all required Python packages with exact versions for reproducibility
"""

import os
import sys
import subprocess

# Exact dependency versions for reproducibility
DEPENDENCIES = [
    'flask==3.0.0',
    'werkzeug==3.0.1',
    'pillow==10.1.0',
    'numpy==1.24.3',
    'opencv-python==4.8.1.78',
    'torch==2.1.0',
    'torchvision==0.16.0',
    'basicsr==1.4.2',
    'realesrgan==0.3.0',
]

def install_dependencies():
    """Install all dependencies in the virtual environment"""
    
    print("Installing dependencies with exact versions...")
    print("This ensures the same versions will be installed even years from now.")
    print()
    
    # Get Python executable from venv
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(os.path.dirname(script_dir), 'Project')
    
    if sys.platform == 'win32':
        python_exe = os.path.join(project_dir, 'venv', 'Scripts', 'python.exe')
        pip_exe = os.path.join(project_dir, 'venv', 'Scripts', 'pip.exe')
    else:
        python_exe = os.path.join(project_dir, 'venv', 'bin', 'python')
        pip_exe = os.path.join(project_dir, 'venv', 'bin', 'pip')
    
    if not os.path.exists(python_exe):
        print(f"ERROR: Virtual environment not found at {python_exe}")
        print("Please run Step 1 first to create the virtual environment.")
        return False
    
    print(f"Using Python: {python_exe}")
    print()
    
    # Install each dependency
    failed_packages = []
    
    for i, package in enumerate(DEPENDENCIES, 1):
        print(f"[{i}/{len(DEPENDENCIES)}] Installing {package}...")
        try:
            result = subprocess.run(
                [pip_exe, 'install', package, '--no-cache-dir'],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                print(f"  ✓ {package} installed successfully")
            else:
                print(f"  ✗ Failed to install {package}")
                print(f"  Error: {result.stderr[:200]}")
                failed_packages.append(package)
        except Exception as e:
            print(f"  ✗ Exception installing {package}: {e}")
            failed_packages.append(package)
        print()
    
    # Summary
    print("=" * 60)
    if failed_packages:
        print(f"Installation completed with {len(failed_packages)} errors:")
        for pkg in failed_packages:
            print(f"  - {pkg}")
        print()
        print("You may need to install these packages manually or check for compatibility issues.")
        return False
    else:
        print("All dependencies installed successfully!")
        return True

if __name__ == '__main__':
    success = install_dependencies()
    sys.exit(0 if success else 1)
