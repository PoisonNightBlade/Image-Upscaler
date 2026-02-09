# AI Image Upscaler 🖼️✨

A free, open-source, offline AI-powered image upscaler that runs entirely on your local machine. No internet required after installation, complete privacy, and professional-quality results.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## ✨ Features

- 🚀 **High-Quality AI Upscaling** - Uses RealESRGAN for professional photorealistic results
- 🔒 **100% Offline & Private** - All processing happens locally (after initial model download)
- 📊 **Dual Upscaling Modes**:
  - **Scale Factor**: Multiply image size by 2x, 3x, 5x, or 10x
  - **Target Resolution**: Set exact dimensions (1080p, 4K, 8K, or custom)
- 🎯 **Smart Non-Stretching** - Intelligent cropping maintains aspect ratio without distortion
- 🖥️ **User-Friendly Web Interface** - Clean, intuitive browser-based UI
- ⚡ **GPU Acceleration** - Automatic CUDA support for faster processing
- 📁 **Multiple Formats** - Supports PNG, JPG, JPEG, WEBP, BMP

## 🎬 How It Works

Upload → Select Mode (Scale Factor or Target Resolution) → Choose Settings → Upscale → Download

Perfect for:
- Enhancing low-resolution photos
- Preparing images for print
- Upscaling for 4K/8K displays
- Restoring old photographs
- Creating high-res assets for projects

## 📋 Prerequisites

- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **4GB+ RAM** (8GB+ recommended for large images)
- **NVIDIA GPU** with CUDA for faster processing

## 🚀 Quick Start (Windows)

### 1. Download or Clone

```bash
git clone https://github.com/poisonnightblade/image-upscaler.git
cd image-upscaler
```

### 2. Run Installation

Double-click `Installation/install.bat` or run:

```bash
cd Installation
install.bat
```

The installer will:
- Create a Python virtual environment
- Install all dependencies
- Download the AI model (47MB)

### 3. Start the Application

Double-click `Project/start.bat` or run:

```bash
cd Project
start.bat
```

The app will automatically open at http://localhost:5000

## 💻 Installation (Linux/macOS)

See [SETUP.md](SETUP.md) for detailed platform-specific instructions.

## 🛠️ Usage

### Scale Factor Mode
1. Upload an image
2. Select "Scale Factor" mode
3. Choose your multiplier (2x, 3x, 5x, or 10x)
4. Click "Upscale Image"
5. Download your enhanced image

### Target Resolution Mode
1. Upload an image
2. Select "Target Resolution" mode
3. Either:
   - Enter custom width and height, OR
   - Click a preset (1080p, 1440p, 4K, 8K)
4. Click "Upscale Image"
5. Download your enhanced image

## 🔧 Technical Details

### How It Works

Uses **RealESRGAN** (Real-ESRGAN: Real-World Blind Super-Resolution), a state-of-the-art AI model trained for:
- Photorealistic upscaling
- Noise reduction
- Detail enhancement
- Artifact removal

### Non-Stretching Algorithm

When using target resolution mode with different aspect ratios:
1. AI upscales to exceed target dimensions
2. Intelligently center-crops to match aspect ratio
3. Final high-quality resize to exact dimensions
4. **Result**: Sharp, undistorted images

### Architecture

- **Backend**: Flask (Python)
- **AI Model**: RealESRGAN (PyTorch)
- **Image Processing**: OpenCV, PIL
- **Frontend**: Vanilla JavaScript, HTML5, CSS3

## 📁 Project Structure

```
image-upscaler/
├── Installation/           # Setup scripts
│   ├── install.bat        # Windows installer
│   ├── step1.py          # Virtual environment setup
│   ├── step2.py          # Dependency installation
│   └── step3.py          # Model download
├── Project/               # Main application
│   ├── backend.py        # Flask server & AI logic
│   ├── start.bat         # Windows launcher
│   ├── models/           # AI model files (created during install)
│   ├── venv/             # Virtual environment (created during install)
│   └── web/              # Frontend files
│       ├── index.html
│       ├── script.js
│       └── styles.css
├── README.md            # This file
└── SETUP.md             # Detailed setup guide
```

## ⚙️ Configuration

### Supported Image Formats
PNG, JPG, JPEG, WEBP, BMP (max 50MB)

### Resolution Limits
- Scale factor mode: Up to 10x original size
- Target resolution mode: Up to 20,000 × 20,000 pixels

### GPU Acceleration
Automatically detects and uses NVIDIA GPUs if CUDA is available. Falls back to CPU if no GPU found.

## 🔧 Troubleshooting

### Common Issues

**"Virtual environment not found"**
→ Run `Installation/install.bat` first

**"Model file not found"**
→ Re-run install.bat and complete Step 3

**Out of memory errors**
→ Use smaller images or scale factors, or close other applications

**Slow processing**
→ Install CUDA for GPU acceleration, or use smaller images

See [SETUP.md#Troubleshooting](SETUP.md#troubleshooting) for more help.

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

### Third-Party Licenses

- **RealESRGAN** - BSD-3-Clause (free for commercial use)
- **BasicSR** - Apache-2.0
- **PyTorch** - BSD-style
- **Flask** - BSD-3-Clause
- **OpenCV** - Apache-2.0

All libraries used in accordance with their respective licenses.

## 🙏 Acknowledgments

- [RealESRGAN](https://github.com/xinntao/Real-ESRGAN) by Xintao Wang et al.
- [BasicSR](https://github.com/XPixelGroup/BasicSR) super-resolution framework
- The open-source community

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📬 Contact

Project Link: [https://github.com/poisonnightblade/image-upscaler](https://github.com/poisonnightblade/image-upscaler)

## ⚠️ Disclaimer

This tool is for personal and educational use. Upscaling cannot add information not in the original image - best results with images that have some existing detail.

---

**Free & Open Source** • **MIT Licensed** • **100% Offline** • **No Data Collection**

If you find this useful, please star the repository! ⭐
