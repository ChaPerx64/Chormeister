#!/bin/bash
cd "$(dirname "$0")"
cd ..

echo "FLUSHING DATABASE..."
python manage.py flush --no-input
echo "FLUSHING DATABASE... DONE"
echo ""

# echo "MAKING MIGRATIONS..."
# python manage.py makemigrations --no-input
# echo "MAKING MIGRATIONS... DONE"
# echo ""

# echo "MIGRATING..."
# python manage.py migrate
# echo "DONE"
# echo ""

# echo "COLLECTING STATICFILES..."
# python manage.py collectstatic --no-input
# echo "DONE"
# echo ""

# echo "CREATING SUPERUSER"
# python manage.py createsuperuser --no-input
# echo "DONE"

echo 'LOADING FROM DUMP FILE...'
python manage.py loaddata ./dumps/dump.json
echo 'LOADING... DONE'
echo ''

echo 'CHECKING...'
python manage.py check
echo 'CHECKING... DONE'

echo "CREATING SUPERUSER"
python manage.py createsuperuser --no-input
echo "DONE"
