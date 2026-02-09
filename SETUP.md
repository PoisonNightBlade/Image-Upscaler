# Setup Guide

## Windows Setup

### Prerequisites
- Python 3.8+ ([Download](https://www.python.org/downloads/))

### Installation

1. **Run the Installer**
   ```
   Double-click: Installation/install.bat
   ```
   
   Or from command line:
   ```cmd
   cd Installation
   install.bat
   ```

2. **Start the Application**
   ```
   Double-click: Project/start.bat
   ```

The app will open at http://localhost:5000

---

## Linux/macOS Setup

### Prerequisites
```bash
# Install Python 3.8+
sudo apt install python3 python3-pip python3-venv  # Ubuntu/Debian
brew install python3  # macOS
```

### Installation

1. **Make scripts executable**
   ```bash
   chmod +x Installation/install.sh
   chmod +x Project/start.sh
   ```

2. **Run installation**
   ```bash
   cd Installation
   ./install.sh
   ```

3. **Start application**
   ```bash
   cd ../Project
   ./start.sh
   ```

---

## Troubleshooting

### "Python not found"
Install Python 3.8 or higher from python.org

### "Virtual environment failed"
Ensure you have `python3-venv` installed:
```bash
sudo apt install python3-venv  # Linux
```

### "Model download failed"
Download manually from:
https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth

Save to: `Project/models/RealESRGAN_x4plus.pth`

### Out of memory
- Close other applications
- Use smaller images
- Use lower scale factors

---

## GPU Acceleration (Optional)

For faster processing with NVIDIA GPUs:

1. Install CUDA Toolkit
2. Install PyTorch with CUDA:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

---

## System Requirements

**Minimum:**
- CPU: Dual-core 2+ GHz
- RAM: 4 GB
- GPU: NVIDIA with 4+ GB VRAM
- Storage: 500 MB

**Recommended:**
- CPU: Quad-core 3+ GHz
- RAM: 8 GB+
- GPU: NVIDIA with 4+ GB VRAM
- Storage: 2 GB

---

See [README.md](README.md) for usage instructions.
