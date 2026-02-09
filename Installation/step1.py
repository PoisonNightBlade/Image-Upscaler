"""
Step 1: Create Virtual Environment
Creates a self-contained Python virtual environment in Project/venv/
"""

import os
import sys
import subprocess
import venv

def create_virtual_environment():
    """Create virtual environment in Project/venv/"""
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(os.path.dirname(script_dir), 'Project')
    venv_path = os.path.join(project_dir, 'venv')
    
    print(f"Project directory: {project_dir}")
    print(f"Virtual environment path: {venv_path}")
    
    # Check if venv already exists
    if os.path.exists(venv_path):
        print("Virtual environment already exists.")
        user_input = input("Do you want to recreate it? (Y/N): ").strip().upper()
        if user_input != 'Y':
            print("Skipping virtual environment creation.")
            return True
        else:
            print("Removing existing virtual environment...")
            import shutil
            shutil.rmtree(venv_path)
    
    # Create virtual environment
    print("Creating virtual environment...")
    try:
        venv.create(venv_path, with_pip=True)
        print("Virtual environment created successfully!")
        
        # Verify Python in venv
        if sys.platform == 'win32':
            python_exe = os.path.join(venv_path, 'Scripts', 'python.exe')
        else:
            python_exe = os.path.join(venv_path, 'bin', 'python')
        
        if os.path.exists(python_exe):
            # Upgrade pip
            print("Upgrading pip...")
            subprocess.run([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                         check=True, capture_output=True)
            print("Pip upgraded successfully!")
            return True
        else:
            print(f"ERROR: Python executable not found at {python_exe}")
            return False
            
    except Exception as e:
        print(f"ERROR creating virtual environment: {e}")
        return False

if __name__ == '__main__':
    success = create_virtual_environment()
    sys.exit(0 if success else 1)
