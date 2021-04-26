"""
WSGI config for buskoin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

SERVER_TYPE = os.environ.get('SERVER_TYPE', None)
if SERVER_TYPE and SERVER_TYPE == 'production':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buskoin.settings.prod")
elif SERVER_TYPE and SERVER_TYPE == 'staging':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buskoin.settings.staging")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buskoin.settings.dev")

application = get_wsgi_application()
