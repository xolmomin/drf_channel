import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.models import Users


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"].get('room_name')
        self.username = self.scope['query_string'].decode()
        if not self.username:
            return
        self.room_group_name = "chat_%s" % self.room_name
        self.from_user = self.scope['user']

        if not self.from_user.pk:
            await self.accept()
            await self.send(text_data=json.dumps({
                'message': 'JWT bilan kiring'
            }))
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    @database_sync_to_async
    def get_list(self):
        return Users.objects.all()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await self.get_list()
        message = text_data_json.get('message')
        if not message:
            await self.send("message not found")
            return

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        data = {
            'message': message,
            'from': self.username
        }
        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))

# ws://10.10.2.88:8000/ws/2
