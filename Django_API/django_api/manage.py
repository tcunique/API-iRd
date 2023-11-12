#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management import execute_from_command_line
from django_api import settings

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_api.settings")
    try:
        # Modifiez la ligne ci-dessous pour utiliser les paramètres de configuration chargés à partir du fichier `.cfg`
        execute_from_command_line([sys.argv[0], 'runserver', f"{settings.SERVER_HOST}:{settings.SERVER_PORT}"])
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

if __name__ == "__main__":
    main()