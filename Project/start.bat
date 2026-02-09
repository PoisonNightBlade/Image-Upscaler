@echo off
setlocal

:: AI Image Upscaler - Runtime Script
echo ============================================================
echo   AI Image Upscaler
echo ============================================================
echo.

:: Change to Project directory
cd /d "%~dp0"

:: Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run install.bat from the Installation folder first.
    echo.
    pause
    exit /b 1
)

:: Check if models are configured
if not exist "models_config.json" (
    echo ERROR: Models configuration not found!
    echo Please run install.bat from the Installation folder first.
    echo.
    pause
    exit /b 1
)

echo Starting application...
echo.
echo Backend server will start on http://localhost:5000
echo Web UI will open in your default browser.
echo.
echo Press Ctrl+C to stop the server.
echo.
echo ============================================================
echo.

:: Activate virtual environment and start backend
call venv\Scripts\activate.bat
python backend.py

pause
