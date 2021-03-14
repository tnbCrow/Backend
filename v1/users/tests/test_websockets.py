import re
import pytest


from django.conf import settings 
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from config.asgi import application

from .test_utils import (
    TEST_USER,
    get_test_user
)

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

@pytest.fixture
def base_settings():
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    return settings

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebsockets:
    async def test_login_user_can_connect_to_wss(self,base_settings):
        user, token = await get_test_user()
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/chat/{user.uuid}/?token={token}'
        )

        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()
    
    async def test_anym_user_cannot_connect_to_wss(self,base_settings):
        user, token = await get_test_user()
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/chat/{user.uuid}/'
        )

        connected, _ = await communicator.connect()
        assert connected is False
        await communicator.disconnect()

    


    