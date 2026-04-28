@echo off
REM Unified Startup Script for The Chronic Pain Hub
REM Starts both Backend API (port 8000) and Frontend Server (port 3000)

title The Chronic Pain Hub - Launcher

echo ========================================
echo  The Chronic Pain Hub - Unified Startup
echo ========================================
echo.
echo This will start:
echo   [1] Backend API on http://localhost:8000
echo   [2] Frontend Server on http://localhost:3000
echo.
echo Available modules after startup:
echo   - Module 1: http://localhost:3000/module1.html
echo   - Module 2: http://localhost:3000/pain-hub-app/
echo   - Module 4: http://localhost:3000/module4.html
echo.
echo ========================================
echo.

REM Check if Backend folder exists
if not exist "Backend\main.py" (
    echo ERROR: Backend\main.py not found!
    pause
    exit /b 1
)

REM Start Backend API in new window
echo Starting Backend API server...
start "Backend API (Port 8000)" cmd /k "cd Backend && echo Starting Backend API... && python main.py"

REM Wait for backend to initialize
echo Waiting for Backend to start...
timeout /t 5 /nobreak > nul

REM Start Frontend Server in current window (so we can see both logs)
echo.
echo Starting Frontend Server...
echo ========================================
python -m http.server 3000
