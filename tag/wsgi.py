
import os
import sys

from django.core.wsgi import get_wsgi_application

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tag.settings")
application = get_wsgi_application()
