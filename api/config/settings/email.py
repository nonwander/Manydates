# Settings mail sending interface via the smtplib module

from .env import env

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = env.str('EMAIL_HOST')
EMAIL_HOST_PASSWORD = env.str('EMAIL_PASS')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
