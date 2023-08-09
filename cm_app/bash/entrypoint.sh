#!/bin/sh

echo "EXECUTING ENTRYPOINT.SH"
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "CHECKING...."
python manage.py check --database default
echo "DONE"
echo ""

echo "MAKING MIGRATIONS..."
python manage.py makemigrations --no-input
echo "MAKING MIGRATIONS... DONE"
echo ""

echo "MIGRATING..."
python manage.py migrate
echo "DONE"
echo ""

echo "COLLECTING STATICFILES..."
python manage.py collectstatic --no-input
echo "DONE"
echo ""

echo "CREATING SUPERUSER"
python manage.py createsuperuser --no-input
echo "DONE"

exec "$@"
