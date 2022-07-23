#!/bin/sh

if [ "$DATABASE" = "dating_clients" ]
then
    echo "Waiting for postgres DB..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "Postgres DB started"
fi

python manage.py flush --no-input
python manage.py migrate
python manage.py createsuperuser --email admin@fake.ru --username admin

exec "$@"