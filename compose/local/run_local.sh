#!/bin/bash

python /code/manage.py makemigrations
#python /code/manage.py makemigrations admin
#python /code/manage.py makemigrations clients
python /code/manage.py migrate
python /code/manage.py collectstatic --noinput
#python manage.py dummy_data_maker
python /code/manage.py runserver --noreload