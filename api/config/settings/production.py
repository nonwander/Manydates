from .base import *
from .email import *

# SECRET_KEY must be generated by the command before the deploy:
# $./generate_secret_key.sh
with open(ROOT_DIR.path('secretkey.txt')) as f:
    SECRET_KEY = f.read().strip()

DEBUG = False

ROOT_URLCONF = 'config.urls'

ALLOWED_HOSTS = [
    env('SERVER_HOST'),
]