import asyncio

import pytest
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart  # noqa
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED

from apps.models import User
from root.asgi import application
from root.settings import MEDIA_ROOT


@pytest.mark.django_db
@pytest.mark.asyncio
class TestWebSocket:
    @pytest.fixture
    def api_client(self):
        from rest_framework.test import APIClient
        return APIClient()

    @database_sync_to_async
    def create_user(self, username, password, email=None):
        return User.objects.create_user(username=username, password=password, email=email)

    @pytest.fixture
    async def sender_data(self, api_client):
        data = {
            'username': 'sender',
            'password': '1'
        }
        user_db = await self.create_user(data['username'], data['password'], 'admin1@mail.ru')
        res = (await sync_to_async(api_client.post)('/api/v1/login', data)).json()
        header = [('authorization', f"Bearer {res['access']}")]
        return user_db, header

    @pytest.fixture
    async def receiver_data(self, api_client):
        data = {
            'username': 'receiver',
            'password': '1'
        }
        user_db = await self.create_user(data['username'], data['password'], 'admin1@mail.ru')
        res = (await sync_to_async(api_client.post)('/api/v1/login', data)).json()
        header = [('authorization', f"Bearer {res['access']}")]
        return user_db, header

    async def test_can_connect_to_server(self, sender_data, receiver_data, api_client):
        sender, s_header = await sender_data
        socket_1 = WebsocketCommunicator(application, '/ws', s_header)
        connected1, _ = await socket_1.connect()
        assert connected1

        receiver, r_header = await receiver_data
        socket_2 = WebsocketCommunicator(application, '/ws', r_header)
        connected2, _ = await socket_2.connect()
        assert connected2

        data = {
            'type': 'msg',
            'msg': 'Hello',
            'user_id': 2
        }
        await socket_1.send_json_to(data)
        res = await socket_1.receive_json_from()
        assert res['is_online']

        await asyncio.sleep(.2)

        res = await socket_2.receive_json_from()
        assert res['msg'] == data['msg']

    async def test_send_file(self, sender_data, receiver_data, api_client):
        sender, s_header = await sender_data
        socket_1 = WebsocketCommunicator(application, '/ws', s_header)
        connected1, _ = await socket_1.connect()
        assert connected1

        receiver, r_header = await receiver_data
        socket_2 = WebsocketCommunicator(application, '/ws', r_header)
        connected2, _ = await socket_2.connect()
        assert connected2

        # TODO oxshamadi )
        image = SimpleUploadedFile('test.png', content=open(MEDIA_ROOT + '/test.png', 'rb').read(),
                                   content_type='image/jpeg')
        data = {'name': image.name, 'file': image.file}
        response = api_client.post(reverse('file-list'), data)
        assert response.status_code == HTTP_201_CREATED

        await socket_1.send_json_to(data)
        res = await socket_1.receive_json_from()
        assert res['is_online']

        await asyncio.sleep(.2)

        res = await socket_2.receive_json_from()
        assert res['msg'] == data['msg']
