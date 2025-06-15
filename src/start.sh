#!/bin/sh

# Ensure data directory exists and has proper permissions
mkdir -p /app/data
chmod -R 777 /app/data

# Run migrations
echo "Running migrations..."
python manage.py makemigrations  --verbosity 2
python manage.py migrate

echo "Running Scripts"
python manage.py init_scripts

# Start server
echo "Starting server..."
gunicorn --bind 0.0.0.0:8080 app.wsgi:application --reload
