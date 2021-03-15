import channels
import pytest
from django.conf import settings 
from rest_framework_simplejwt.tokens import AccessToken
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from config.asgi import application

from .test_utils import (
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
class TestWebsocketsAuth:
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
            path=f'/chat/{user.uuid}/?token=faketoken'
        )

        connected, _ = await communicator.connect()
        assert connected is False
        await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebsocketsChat:
    async def test_user_can_receive_message(self):
        user, token = await get_test_user()
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/chat/{user.uuid}/?token={token}'
        )

        connected, _ = await communicator.connect()
        message = {
            'type': 'chat.message',
            'data': 'This is a test message.',
        }

        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            f'chat_group_{user.uuid}',
            message=message
        )

        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()
        # assert 1==11
    


    