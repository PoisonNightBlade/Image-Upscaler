"""
Step 2: Install Dependencies
Smart GPU-aware installer with external-drive safe temp + cache handling.
Installs the most ideal stable PyTorch build (not latest).
"""

import os
import sys
import subprocess
import re

# ===============================
# General Dependencies (no torch)
# ===============================

DEPENDENCIES = [
    'flask==3.0.0',
    'werkzeug==3.0.1',
    'pillow==10.1.0',
    'numpy==1.24.3',
    'opencv-python==4.8.1.78',
    'basicsr==1.4.2',
    'realesrgan==0.3.0',
]

# Stable PyTorch pairing (locked version)
TORCH_VERSION = "2.1.0"
TORCHVISION_VERSION = "0.16.0"

# ===============================
# GPU Detection
# ===============================

def detect_cuda_version():
    try:
        result = subprocess.run(
            ["nvidia-smi"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return None

        match = re.search(r"CUDA Version:\s+(\d+\.\d+)", result.stdout)
        if match:
            return float(match.group(1))

    except Exception:
        pass

    return None


def choose_torch_build():
    cuda_version = detect_cuda_version()

    if cuda_version is None:
        print("Could not automatically detect NVIDIA GPU.")
        user_input = input("Do you have an NVIDIA GPU? (y/n): ").strip().lower()

        if user_input == "y":
            print("\nInstalling safe default CUDA 11.8 build...")
            return "cu118"
        else:
            return "cpu"

    print(f"Detected CUDA support from driver: {cuda_version}")

    if cuda_version >= 12.0:
        return "cu121"
    else:
        return "cu118"


# ===============================
# Installation Logic
# ===============================

def install_dependencies():

    print("\nInstalling dependencies with smart GPU detection...\n")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(os.path.dirname(script_dir), 'Project')

    if sys.platform == 'win32':
        pip_exe = os.path.join(project_dir, 'venv', 'Scripts', 'pip.exe')
    else:
        pip_exe = os.path.join(project_dir, 'venv', 'bin', 'pip')

    if not os.path.exists(pip_exe):
        print("ERROR: Virtual environment not found.")
        print("Run Step 1 first.")
        return False

    # ======================================
    # Force temp + cache to external folder
    # ======================================

    external_temp = os.path.join(project_dir, "temp")
    external_cache = os.path.join(project_dir, "pip_cache")

    os.makedirs(external_temp, exist_ok=True)
    os.makedirs(external_cache, exist_ok=True)

    env = os.environ.copy()
    env["TMP"] = external_temp
    env["TEMP"] = external_temp
    env["PIP_CACHE_DIR"] = external_cache

    failed_packages = []

    # -----------------------
    # Install normal packages
    # -----------------------

    for i, package in enumerate(DEPENDENCIES, 1):
        print(f"\n[{i}/{len(DEPENDENCIES)}] Installing {package}...\n")
        result = subprocess.run([
            pip_exe,
            "install",
            package,
            "--progress-bar=on",
            "--no-cache-dir",
            "--disable-pip-version-check"
        ], env=env)

        if result.returncode != 0:
            failed_packages.append(package)

    # -----------------------
    # Install PyTorch
    # -----------------------

    build = choose_torch_build()

    print("\nInstalling PyTorch...\n")

    if build == "cpu":
        print("Installing CPU-only PyTorch (stable build)...\n")

        result = subprocess.run([
            pip_exe,
            "install",
            f"torch=={TORCH_VERSION}",
            f"torchvision=={TORCHVISION_VERSION}",
            "--progress-bar=on",
            "--no-cache-dir",
            "--disable-pip-version-check"
        ], env=env)

        if result.returncode != 0:
            failed_packages.extend(["torch", "torchvision"])

    else:
        print(f"Installing CUDA-enabled PyTorch ({build})...\n")

        index_url = f"https://download.pytorch.org/whl/{build}"

        result = subprocess.run([
            pip_exe,
            "install",
            f"torch=={TORCH_VERSION}+{build}",
            f"torchvision=={TORCHVISION_VERSION}+{build}",
            "--index-url", index_url,
            "--progress-bar=on",
            "--no-cache-dir",
            "--disable-pip-version-check"
        ], env=env)

        if result.returncode != 0:
            failed_packages.extend(["torch", "torchvision"])

    # -----------------------
    # Summary
    # -----------------------

    print("\n" + "=" * 60)

    if failed_packages:
        print("Installation completed with errors:")
        for pkg in failed_packages:
            print(f"  - {pkg}")
        return False
    else:
        print("All dependencies installed successfully!")
        print("Environment is fully ready.\n")

        # Optional verification
        print("Verifying PyTorch installation...\n")
        verify = subprocess.run([
            os.path.join(project_dir, 'venv', 'Scripts', 'python.exe')
            if sys.platform == 'win32'
            else os.path.join(project_dir, 'venv', 'bin', 'python'),
            "-c",
            "import torch; print('CUDA Available:', torch.cuda.is_available())"
        ], env=env)

        return True


if __name__ == '__main__':
    success = install_dependencies()
    sys.exit(0 if success else 1)
