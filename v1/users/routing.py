from django.urls import re_path,path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('chat/<str:chat_room>/',ChatConsumer.as_asgi(),name="chat_room"),
]