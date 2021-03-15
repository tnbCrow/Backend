import os

from django.core.asgi import get_asgi_application

# change the config.development to your required setting module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

application = get_asgi_application()
