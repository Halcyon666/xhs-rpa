@echo off
cd /d "%~dp0"

echo ========================================
echo Starting Dedicated Browser...
echo ========================================

set "CHROME_PATH="

REM 1. Try to find Chrome in Registry
for /f "tokens=2*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" /ve 2^>nul') do set "CHROME_PATH=%%b"

REM 2. Fallback to common paths
if not defined CHROME_PATH (
    if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set "CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe"
)
if not defined CHROME_PATH (
    if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" set "CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)
if not defined CHROME_PATH (
    if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" set "CHROME_PATH=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
)

REM 3. Check if found
if not defined CHROME_PATH (
    echo [ERROR] Google Chrome not found!
    echo Please install Chrome or modify the path in this script manually.
    pause
    exit /b 1
)

echo [INFO] Chrome Path: "%CHROME_PATH%"
echo [INFO] User Data Dir: "%~dp0chrome-profile"

REM Create profile directory if not exists
if not exist "%~dp0chrome-profile" mkdir "%~dp0chrome-profile"

REM 4. Start Browser
start "" "%CHROME_PATH%" --remote-debugging-port=9222 --user-data-dir="%~dp0chrome-profile" --no-first-run --no-default-browser-check

if errorlevel 1 (
    echo [ERROR] Failed to start Chrome!
    pause
    exit /b 1
)

echo ========================================================
echo [IMPORTANT] Please login to Xiaohongshu in the opened browser.
echo KEEP THE BROWSER OPEN after login!
echo ========================================================
pause