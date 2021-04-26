#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    SERVER_TYPE = os.environ.get('SERVER_TYPE', None)
    if SERVER_TYPE and SERVER_TYPE == 'production':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buskoin.settings.prod")
    elif SERVER_TYPE and SERVER_TYPE == 'staging':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buskoin.settings.staging")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buskoin.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
