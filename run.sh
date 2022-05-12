#!/bin/bash

export DJANGO_READ_DOT_ENV_FILE=True
export SERVER_IP=2.57.187.13
export SERVER_HOST=XXX
./generate_secret_key.sh
python ./api/manage.py makemigrations
python ./api/manage.py migrate
python ./api/manage.py collectstatic
#python ./api/manage.py dummy_data_maker
python ./api/manage.py runserver --noreload --insecure
