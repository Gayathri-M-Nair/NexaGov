@echo off
REM Quick test script for Windows

echo Testing Brahma Lite Chatbot...
echo.

REM Check if server is running
curl -s http://localhost:4002/ >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Server not running on http://localhost:4002
    echo Please start it with: run.bat
    pause
    exit /b 1
)

echo [OK] Server is running
echo.

echo Testing endpoints...
echo.

REM Health check
echo 1. Health Check:
curl -s http://localhost:4002/
echo.
echo.

REM Test chat
echo 2. Chat Test - "hi":
curl -s -X POST http://localhost:4002/chat -H "Content-Type: application/json" -d "{\"message\": \"hi\"}"
echo.
echo.

echo 3. Chat Test - "what is brahma":
curl -s -X POST http://localhost:4002/chat -H "Content-Type: application/json" -d "{\"message\": \"what is brahma\"}"
echo.
echo.

REM Stats
echo 4. Stats:
curl -s http://localhost:4002/stats
echo.
echo.

echo ========================================
echo Tests complete!
echo ========================================
pause
