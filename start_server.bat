@echo off
echo ========================================
echo Starting Chronic Pain Hub Backend Server
echo ========================================
echo.

cd /d "%~dp0Backend"

echo Checking Python environment...
python --version
echo.

echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
