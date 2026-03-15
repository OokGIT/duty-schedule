"""
WSGI config for duty_schedule project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'duty_schedule.settings')

application = get_wsgi_application()
