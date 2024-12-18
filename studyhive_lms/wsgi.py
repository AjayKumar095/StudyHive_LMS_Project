"""
WSGI config for studyhive_lms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

# Add the project directory to sys.path (the parent directory of this wsgi.py file)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studyhive_lms.settings")

application = get_wsgi_application()
