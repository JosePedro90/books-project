#!/bin/bash

# Function to check if the database is ready
wait_for_db() {
  echo "Waiting for database to be ready..."
  until PGPASSWORD=$DATABASE_PASSWORD psql -h "$DATABASE_HOST" -U "$DATABASE_USER" -d "$DATABASE_NAME" -c '\q'; do
    echo "Database is unavailable - sleeping"
    sleep 5
  done
  echo "Database is ready!"
}

# Wait for the database to be ready
wait_for_db

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser
echo "Creating superuser..."
if ! python manage.py createsuperuser --username=admin --email=admin@example.com --noinput; then
  echo "Superuser 'admin' already exists."
else
  echo "Superuser 'admin' created successfully."
fi
# Run Celery worker
echo "Starting Celery worker..."
celery -A config.celery worker --loglevel=info -c 4 &

# Run Django development server
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
