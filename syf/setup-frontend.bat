@echo off
echo ========================================
echo Forum Frontend Setup Script
echo ========================================
echo.

cd frontend

echo Installing dependencies...
echo This may take a few minutes...
echo.

npm install
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Frontend Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure backend is running (run start-backend.bat)
echo 2. Run start-frontend.bat to start the frontend server
echo.
pause
