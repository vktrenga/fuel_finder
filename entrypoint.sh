#!/bin/sh

echo "Waiting for Postgres..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Postgres started!"

echo "Running makemigrations..."
python manage.py makemigrations --noinput

echo "Running migrate..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Loading initial data..."
python manage.py runscript initial_data || echo "Script failed or not found"

echo "Starting Gunicorn..."
exec gunicorn fuel_finder.wsgi:application --bind 0.0.0.0:8000
