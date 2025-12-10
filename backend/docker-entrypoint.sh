#!/bin/bash
set -e

echo "Starting Django application..."

# Function to wait for database
wait_for_db() {
    echo "Waiting for database to be ready..."
    
    # Extract database connection details from DATABASE_URL
    if [ -n "$DATABASE_URL" ]; then
        # Wait up to 60 seconds for database
        for i in {1..60}; do
            if python << END
import os
import psycopg2
from urllib.parse import urlparse

db_url = os.environ.get('DATABASE_URL')
if db_url:
    result = urlparse(db_url)
    try:
        conn = psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        conn.close()
        print("Database is ready!")
        exit(0)
    except psycopg2.OperationalError:
        exit(1)
END
            then
                echo "Database connection successful!"
                return 0
            fi
            echo "Database not ready yet, waiting... ($i/60)"
            sleep 1
        done
        
        echo "ERROR: Database did not become ready in time"
        exit 1
    else
        echo "Using SQLite, skipping database wait"
    fi
}

# Wait for database
wait_for_db

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create logs directory
mkdir -p logs

echo "Starting application with: $@"

# Execute the main command
exec "$@"

