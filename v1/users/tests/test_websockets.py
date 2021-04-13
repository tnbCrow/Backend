from django.contrib.auth import get_user_model
import pytest
from django.conf import settings
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from config.asgi import application
from channels.db import database_sync_to_async

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


# @pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebsocketsAuth:
    async def test_login_user_can_connect_to_wss(self, base_settings):
        user, token = await get_test_user_async()
        thread = await get_test_thread_async(user)

        communicator = WebsocketCommunicator(
            application=application,
            path=f'/chat/{thread.uuid}/?token={token}'
        )

        connected, _ = await communicator.connect()
        await communicator.disconnect()
        assert connected is True

    async def test_anym_user_cannot_connect_to_wss(self, base_settings):
        user, _ = await get_test_user_async()
        thread = await get_test_thread_async(user)

        communicator = WebsocketCommunicator(
            application=application,
            path=f'/chat/{thread.uuid}/?token=faketoken'
        )

        connected, _ = await communicator.connect()
        await communicator.disconnect()
        assert connected is False

    async def test_cannot_connect_to_invalid_thread(self):
        _, token = await get_test_user_async()
        fake_uuid = '2b375eed-8e14-4bdf-ac09-bf44563061da'

        communicator = WebsocketCommunicator(
            application=application,
            path=f'/chat/{fake_uuid}/?token={token}'
        )

        connected, _ = await communicator.connect()
        await communicator.disconnect()
        assert connected is False



@pytest.mark.skip(reason="no way of currently testing this")
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
