@echo off
REM Brahma Lite Chatbot - Windows Startup Script
REM Optimized for 1-2GB RAM systems

echo ========================================
echo   Brahma Lite Chatbot - Starting...
echo ========================================
echo.

REM Set memory-efficient environment
set OMP_NUM_THREADS=2
set PYTHONUNBUFFERED=1

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if server is already running on port 4002
netstat -ano | findstr :4002 > nul
if %errorlevel% equ 0 (
    echo [WARNING] Port 4002 is already in use
    echo Kill the process and try again
    pause
    exit /b 1
)

echo [OK] Starting Brahma Lite on port 4002...
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start uvicorn server
python -m uvicorn app.main:app --host 0.0.0.0 --port 4002 --workers 1 --log-level info

echo.
echo Server stopped.
pause
