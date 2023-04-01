from datetime import datetime

import ujson
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import Q

from apps.models import Users, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    groups = 'groups'
    __format_data = '%Y-%m-%d %H:%M:%S'

    async def connect(self):
        self.from_user = self.scope['user']

        if self.from_user.is_anonymous:
            await self.accept()
            response = {
                'message': 'JWT bilan kiring'
            }
            await self.send_json(response)
            await self.close()
        else:
            await self.channel_layer.group_add(self.groups, self.channel_name)
            await self.accept()
            await self.notify_user_status(True)
        return

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.groups, self.channel_name)
        if self.from_user.is_authenticated:
            await self.notify_user_status(False)

    async def send_error_msg(self, msg: str):
        res = {
            'message': msg
        }
        await self.send_json(res)

    async def receive_json(self, content, *args):
        await self.get_list()
        message = content.get('message')
        user_id = content.get('user_id')
        self.to_user = await self.get_user(user_id)

        if not message:
            await self.send_error_msg('xabar yoq')
            return

        if not self.to_user:
            await self.send_error_msg('userni kiriting')
            return

        if not self.to_user:
            await self.send_error_msg('bunday odam yoqku')
            return

        msg = await self.save_message(self.from_user.id, self.to_user.id, message)
        created_at = datetime.strftime(msg.created_at, self.__format_data)

        await self.channel_layer.group_send(
            self.groups, {
                'type': 'chat.message',
                'message': msg.message,
                'to_user': msg.sender_id,
                'from_user': msg.receiver_id,
                'created_at': created_at
            }
        )

    @database_sync_to_async  # ✅
    def save_message(self, from_user: int, to_user: int, message: str):
        return Message.objects.create(sender_id=from_user, receiver_id=to_user, message=message)

    @database_sync_to_async  # ✅
    def get_user(self, pk) -> bool:
        return Users.objects.filter(pk=pk).first()

    @database_sync_to_async
    def get_list(self):
        return Users.objects.all()

    async def notify_user_status(self, is_online: bool):
        await self.channel_layer.group_send(
            self.groups,
            {
                'type': 'chat.change.status',
                'user': {
                    'id': self.from_user.id,
                    'username': self.from_user.username
                },
                'is_online': is_online,
            }
        )

    @database_sync_to_async
    def check_user_chat(self, to_user, from_id):
        return Message.objects.filter(
            Q(receiver=to_user) & Q(sender=from_id) |
            Q(receiver=from_id) & Q(sender=to_user)
        ).exists()

    @database_sync_to_async
    def update_user_status(self, user, is_online=False) -> None:
        user.is_online = is_online
        user.save()
        print(f"{user.phone_number}- {user.id} -- {'online' if is_online else 'offline'}")

    async def chat_change_status(self, event):
        if self.from_user.pk != event['user']['id']:
            # and await self.check_user_chat(self.from_user.id, event['user_id']):
            # print(self.from_user.pk, event['user_id'])
            data = {
                'type': 'status',
                'is_online': event['is_online'],
                'user': {
                    'id': event['user']['id'],
                    'username': event['user']['username']
                }
            }

            await self.send(ujson.dumps(data))
            return

    async def chat_message(self, event):
        message = event['message']
        from_user = event['from_user']
        if self.from_user.pk == event['to_user'] or self.from_user.pk == from_user:
            data = {
                'message': message,
                'from': from_user,
                'created_at': event['created_at']
            }
            await self.send_json(data)

    @classmethod
    async def decode_json(cls, content):
        try:
            return ujson.loads(content)
        except Exception as e:
            print(content, e, 'XATOLIK')

    @classmethod
    async def encode_json(cls, content):
        try:
            return ujson.dumps(content)
        except Exception as e:
            print(content, e, 'XATOLIK')

# ws://10.10.2.88:8000/ws
