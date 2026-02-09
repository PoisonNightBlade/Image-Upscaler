@echo off
setlocal enabledelayedexpansion

:: AI Image Upscaler - Installation Script
echo ============================================================
echo   AI Image Upscaler - Installation
echo ============================================================
echo.

:: Change to the Installation directory
cd /d "%~dp0"

:: Step Selection
echo Select which steps to execute:
echo [1] All steps (default)
echo [2] Step 1 only - Create virtual environment
echo [3] Step 2 only - Install dependencies
echo [4] Step 3 only - Download AI model
echo [5] Custom combination
echo.
set /p STEP_CHOICE="Enter your choice (1-5, default=1): "
if "%STEP_CHOICE%"=="" set STEP_CHOICE=1

:: Setup Type Selection
echo.
echo Select setup type:
echo [1] Local Setup - Everything stored in Project folder (default)
echo [2] External Setup - Specify custom path for models
echo.
set /p SETUP_TYPE="Enter your choice (1-2, default=1): "
if "%SETUP_TYPE%"=="" set SETUP_TYPE=1

set "MODELS_PATH=..\Project\models"
if "%SETUP_TYPE%"=="2" (
    set /p CUSTOM_PATH="Enter full path for models storage: "
    set "MODELS_PATH=!CUSTOM_PATH!"
    echo !MODELS_PATH! > config_paths.txt
) else (
    if exist config_paths.txt del config_paths.txt
)

:: Determine which steps to run
set RUN_STEP1=0
set RUN_STEP2=0
set RUN_STEP3=0

if "%STEP_CHOICE%"=="1" (
    set RUN_STEP1=1
    set RUN_STEP2=1
    set RUN_STEP3=1
) else if "%STEP_CHOICE%"=="2" (
    set RUN_STEP1=1
) else if "%STEP_CHOICE%"=="3" (
    set RUN_STEP2=1
) else if "%STEP_CHOICE%"=="4" (
    set RUN_STEP3=1
) else if "%STEP_CHOICE%"=="5" (
    echo.
    set /p RUN_STEP1="Run Step 1? (Y/N): "
    set /p RUN_STEP2="Run Step 2? (Y/N): "
    set /p RUN_STEP3="Run Step 3? (Y/N): "
    if /i "!RUN_STEP1!"=="Y" set RUN_STEP1=1
    if /i "!RUN_STEP2!"=="Y" set RUN_STEP2=1
    if /i "!RUN_STEP3!"=="Y" set RUN_STEP3=1
)

echo.
echo ============================================================
echo Starting installation...
echo ============================================================
echo.

:: Step 1: Create virtual environment
if "%RUN_STEP1%"=="1" (
    echo [STEP 1] Creating virtual environment...
    python step1.py
    if errorlevel 1 (
        echo [ERROR] Step 1 failed!
        pause
        exit /b 1
    )
    echo [SUCCESS] Step 1 completed.
    echo.
)

:: Step 2: Install dependencies
if "%RUN_STEP2%"=="1" (
    echo [STEP 2] Installing dependencies...
    ..\Project\venv\Scripts\python.exe step2.py
    if errorlevel 1 (
        echo [ERROR] Step 2 failed!
        pause
        exit /b 1
    )
    echo [SUCCESS] Step 2 completed.
    echo.
)

:: Step 3: Download AI model
if "%RUN_STEP3%"=="1" (
    echo [STEP 3] Setting up AI model...
    ..\Project\venv\Scripts\python.exe step3.py "%MODELS_PATH%"
    if errorlevel 1 (
        echo [ERROR] Step 3 failed!
        pause
        exit /b 1
    )
    echo [SUCCESS] Step 3 completed.
    echo.
)

echo ============================================================
echo Installation completed successfully!
echo ============================================================
echo.
echo To start the application, run start.bat in the Project folder.
echo.
pause
