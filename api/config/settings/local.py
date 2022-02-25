from .base import *

SECRET_KEY = env('DJANGO_SECRET_KEY', default='cbx3f9d_^+9d0@@zcr&^wg8wdv&b$jvju79==^sy%f()p&2bp3')

DEBUG = env.bool('DJANGO_DEBUG', default=True)

ALLOWED_HOSTS = [
    '0.0.0.0', '127.0.0.1', 'localhost',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ROOT_URLCONF = 'config.urls_dev'

# Django Debug ToolBar settings
INTERNAL_IPS = [
    '127.0.0.1', 'localhost',
]
INSTALLED_APPS += [
    'debug_toolbar',
]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': env.db('DB_ENGINE'),
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT'),
        }
    }
