import pytest
from django.conf import settings
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from config.asgi import application

from v1.thread.models import ChatThread

from .test_utils import (
    get_test_user_async,
    get_test_thread_async,
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
    async def test_login_user_can_connect_to_wss(self, base_settings):
        user, token = await get_test_user_async()
        print(user,type(user))
        thread = await get_test_thread_async(user1=user)

        communicator = WebsocketCommunicator(
            application=application,
            path=f'/chat/{thread.uuid}/?token={token}'
        )

        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_anym_user_cannot_connect_to_wss(self, base_settings):
        user, token = await get_test_user_async()
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
        user, token = await get_test_user_async()
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
