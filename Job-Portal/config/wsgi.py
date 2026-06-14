import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apps')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
