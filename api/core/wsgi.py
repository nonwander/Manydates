#!/usr/local/bin python3
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.core.settings.production')
application = get_wsgi_application()
