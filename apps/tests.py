import pytest
from channels.testing import WebsocketCommunicator
from django.test import Client

from apps.consumers import ChatConsumer
from apps.models import User


@pytest.mark.asyncio
class TestWebSocket:

    @pytest.fixture
    def user(self):
        user = User.objects.create_user('admin', 'admin@mail.ru', '1')
        return user

    async def test_websocket_connection(self, client: Client, user):
        client.force_login(await user)
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/test/")
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()
