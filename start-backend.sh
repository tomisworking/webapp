#!/bin/bash

echo "========================================"
echo "Starting Forum Backend Server"
echo "========================================"
echo ""

cd backend

echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Starting Django development server..."
echo "Backend will be available at: http://localhost:8000"
echo "Admin panel at: http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
