#!/bin/sh

echo $POSTGRES_HOST
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 1.0
    done

    echo "PostgreSQL started"
fi

# echo "CHECKING...."
# python manage.py check --database default
# echo "CHECKING.... DONE"

# echo "\n\nFLUSHING..."
# python manage.py flush --no-input
# echo "making migrations..."
# python manage.py makemigrations
echo "migrating..."
python manage.py migrate



exec "$@"
