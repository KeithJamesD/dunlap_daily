@echo off
echo 🚀 Starting Dunlap Daily Local Server...
echo ===========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo 📥 Please install Python first:
    echo    1. Visit: https://python.org/downloads/
    echo    2. Download and install Python 3.8 or newer
    echo    3. Make sure to check "Add Python to PATH" during installation
    echo    4. Restart this script after installation
    echo.
    pause
    exit /b 1
)

REM Check if required packages are installed
echo 📦 Checking dependencies...
python -c "import feedgen, docx, pytz, requests" 2>nul
if errorlevel 1 (
    echo 📦 Installing required packages...
    pip install python-docx feedgen pytz requests
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✅ Dependencies ready!
echo.

python run_local.py

echo.
echo Press any key to exit...
pause > nul