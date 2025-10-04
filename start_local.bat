@echo off
echo 🥭 Mango Disease Detection API - Local Development
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.9+ first
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if we're in the right directory
if not exist "main.py" (
    echo ❌ main.py not found. Please run this from the railway_deployment folder
    pause
    exit /b 1
)

echo ✅ In correct directory
echo.

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

REM Run deployment test
echo 🧪 Running deployment tests...
python test_deployment.py
echo.

REM Ask if user wants to start the server
set /p choice="🚀 Start the local server? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo 🌟 Starting Mango Disease Detection API...
    echo.
    echo 🌐 Web Interface: http://localhost:8000
    echo 📚 API Docs: http://localhost:8000/docs  
    echo 💚 Health Check: http://localhost:8000/health
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    python main.py
) else (
    echo.
    echo 💡 To start the server manually, run: python main.py
)

pause