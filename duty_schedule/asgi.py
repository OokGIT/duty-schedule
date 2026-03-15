"""
ASGI config for duty_schedule project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'duty_schedule.settings')

application = get_asgi_application()
