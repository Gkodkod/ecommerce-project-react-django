#!/bin/bash

set -e

# Wait for postgres to be ready to accept connections
echo "Waiting for postgres..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "Postgres is unavailable — sleeping"
  sleep 1
done
echo "PostgreSQL is ready."

# Apply database migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Start development server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
