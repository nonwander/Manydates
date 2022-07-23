#!/bin/bash

#set -o errexit
#set -o pipefail
#set -o nounset

python3 /code/manage.py makemigrations
python3 /code/manage.py migrate
python3 /code/manage.py collectstatic --noinput
#python /code/manage.py dummy_data_maker
/usr/local/bin/gunicorn api.core.wsgi:application --bind 0.0.0.0:8000 --chdir=/code