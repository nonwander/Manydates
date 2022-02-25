"""
The correct settings file (production.py, local.py)
is chosen at runtime according to the system's hostname/host's ip
or DJANGO_SECRET_KEY variable in .env file.

=====================
 Local customization
=====================
Local settings are used by developers.
Django debug toolbar is used for debugging.
The project is launched on a local machine by default.
Django's secret key is set in the settings by default,
or you can write your own in .env file as DJANGO_DEBUG variable.

==========================
 Production customization
==========================
The settings for production are used on the combat server
in the Docker container and only with the Debug=FALSE.
Django's secret key is generated directly when mounting
the docker-image once, you don't need to keep it in secrets.

===========================
 Settings inheritance flow
===========================

                 --> local.py
                /   \
        _init_.py    }<-- base.py <-- env.py
                \   /
                 --> production.py
                     ^-- email.py
"""

import os
import socket
import sys

from .env import env

PRODUCTION_HOSTNAME = env('SERVER_HOST')
PRODUCTION_IP = env('SERVER_IP')
CURRENT_HOSTNAME = socket.gethostname()
CURRENT_HOSTIP = socket.gethostbyname(socket.getfqdn())
is_hostname = CURRENT_HOSTNAME == PRODUCTION_HOSTNAME
is_hostip = CURRENT_HOSTIP == PRODUCTION_IP

try:
    if is_hostname or is_hostip:
        print('Loading production settings file')
        from .production import *
    else:
        print('Loading dev settings file')
        os.environ['DJANGO_READ_DOT_ENV_FILE'] = 'True'
        from .local import *
except ImportError as err:
    err_message = err.message
    sys.stderr.write(
        f('Error: There was an error importing the correct settings file.\n') +
        f('Error message: {err_message}')
    )
    sys.exit(1)
