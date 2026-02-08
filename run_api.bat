@echo off
cd /d "%~dp0"

echo ========================================
echo XHS RPA - API Server Mode
echo ========================================

REM 1. Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python.
    pause
    exit /b 1
)

REM 2. Setup Venv
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Creating venv...
    python -m venv venv
)

REM 3. Activate Venv
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate venv!
    pause
    exit /b 1
)

REM 4. Install Dependencies (Simple check)
echo [INFO] Installing dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [WARN] Fast install failed, trying verbose install...
    pip install fastapi uvicorn aiohttp playwright pyyaml Pillow
)

REM 5. Run Server
echo.
echo [INFO] Starting API Server on Port 8000...
echo [INFO] Please ensure 'start_browser.bat' is running.
echo.

python src/server.py

if errorlevel 1 (
    echo.
    echo [ERROR] Server exited with error!
    pause
)

pause