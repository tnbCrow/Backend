import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter

# change the config.development to your required setting module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# websocket 
from v1.users.routing import websocket_urlpatterns
from v1.users.middleware import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":TokenAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ) 
})