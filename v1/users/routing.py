from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]