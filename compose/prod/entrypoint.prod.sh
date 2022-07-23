#!/bin/sh

if [ "$DATABASE" = "dating_clients" ]
then
    echo "Waiting for PostgreSQL DB..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 1
    done

    echo "Postgres DB is available"
fi

exec "$@"