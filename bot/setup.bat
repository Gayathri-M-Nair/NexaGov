@echo off
REM Brahma Lite Chatbot - Windows Setup Script

echo ========================================
echo   Brahma Lite Chatbot - Setup
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] Pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Check .env file
if not exist ".env" (
    echo [WARNING] .env file not found
    if exist ".env.example" (
        echo Creating .env from .env.example...
        copy .env.example .env
        echo.
        echo [IMPORTANT] Please edit .env and add your GOOGLE_API_KEY
    ) else (
        echo Please create a .env file with your GOOGLE_API_KEY
    )
    echo.
)

REM Check data files
if not exist "data\events.json" (
    echo [WARNING] data\events.json not found
    echo Please copy your events.json to the data folder
    echo.
)

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env and add your GOOGLE_API_KEY (if not done)
echo 2. Run: run.bat
echo.
echo For manual start:
echo   venv\Scripts\activate.bat
echo   python -m uvicorn app.main:app --host 0.0.0.0 --port 4002
echo.
pause
