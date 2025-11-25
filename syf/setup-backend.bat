@echo off
echo ========================================
echo Forum Backend Setup Script
echo ========================================
echo.

cd backend

echo Step 1/7: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo Step 2/7: Activating virtual environment...
call venv\Scripts\activate

echo.
echo Step 3/7: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 4/7: Creating migrations for users app...
python manage.py makemigrations users
if errorlevel 1 (
    echo ERROR: Failed to create users migrations
    pause
    exit /b 1
)

echo.
echo Step 5/7: Creating migrations for forum app...
python manage.py makemigrations forum
if errorlevel 1 (
    echo ERROR: Failed to create forum migrations
    pause
    exit /b 1
)

echo.
echo Step 6/7: Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo.
echo Step 7/7: Creating superuser...
echo Please enter admin credentials:
python manage.py createsuperuser

echo.
echo Loading sample data...
python manage.py seed_data

echo.
echo ========================================
echo Backend Setup Complete!
echo ========================================
echo.
echo Test user credentials (password: password123):
echo   - alice@example.com
echo   - bob@example.com
echo   - charlie@example.com
echo.
echo Next steps:
echo 1. Run start-backend.bat to start the backend server
echo 2. Setup the frontend by running setup-frontend.bat
echo.
pause
