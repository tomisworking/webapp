#!/bin/bash

echo "========================================"
echo "Forum Backend Setup Script"
echo "========================================"
echo ""

cd backend

echo "Step 1/7: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo ""
echo "Step 2/7: Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Step 3/7: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "Step 4/7: Creating migrations for users app..."
python manage.py makemigrations users
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create users migrations"
    exit 1
fi

echo ""
echo "Step 5/7: Creating migrations for forum app..."
python manage.py makemigrations forum
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create forum migrations"
    exit 1
fi

echo ""
echo "Step 6/7: Running database migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to run migrations"
    exit 1
fi

echo ""
echo "Step 7/7: Creating superuser..."
echo "Please enter admin credentials:"
python manage.py createsuperuser

echo ""
echo "Loading sample data..."
python manage.py seed_data

echo ""
echo "========================================"
echo "Backend Setup Complete!"
echo "========================================"
echo ""
echo "Test user credentials (password: password123):"
echo "  - alice@example.com"
echo "  - bob@example.com"
echo "  - charlie@example.com"
echo ""
echo "Next steps:"
echo "1. Run ./start-backend.sh to start the backend server"
echo "2. Setup the frontend by running ./setup-frontend.sh"
echo ""
