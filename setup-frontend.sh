#!/bin/bash

echo "========================================"
echo "Forum Frontend Setup Script"
echo "========================================"
echo ""

cd frontend

echo "Installing dependencies..."
echo "This may take a few minutes..."
echo ""

npm install
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo "Frontend Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Make sure backend is running (./start-backend.sh)"
echo "2. Run ./start-frontend.sh to start the frontend server"
echo ""
