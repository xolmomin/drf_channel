from datetime import datetime

import ujson
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import Q

from apps.models import Message, User


class BaseAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    @classmethod
    async def decode_json(cls, data):
        try:
            return ujson.loads(data)
        except Exception as e:
            print(data, e, 'XATOLIK')

    @classmethod
    async def encode_json(cls, data):
        try:
            return ujson.dumps(data)
        except Exception as e:
            print(data, e, 'XATOLIK')

    async def send_error(self, msg: str):
        await self.send_json({'msg': msg})


class ChatConsumer(BaseAsyncJsonWebsocketConsumer):
    groups = 'groups'
    __format_data = '%Y-%m-%d %H:%M:%S'

    async def connect(self):
        self.from_user = self.scope['user']
        await self.accept()

        if self.from_user.is_anonymous:
            await self.send_error('JWT bilan kiring')
            await self.close()
        else:
            await self.channel_layer.group_add(self.groups, self.channel_name)
            await self.notify_user_status()

        return

    async def send_message(self, sender_id: int, receiver_id: int, msg_id: int):
        await self.channel_layer.group_send(
            self.groups, {
                'type': 'send_read_msg',
                'from_user': sender_id,
                'to_user': receiver_id,
                'msg_id': msg_id
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.groups, self.channel_name)
        if self.from_user.is_authenticated:
            await self.notify_user_status(False)

    async def file_type(self, data: dict):
        file = data.get('file')
        if not file:
            await self.send_error('file yoq')

        if not self.to_user:
            await self.send_error('userni kiriting')
            return

        if not self.to_user:
            await self.send_error('bunday odam yoqku')
            return

    async def msg_type(self, data):
        msg = data.get('msg')

        if not msg:
            await self.send_error('xabar yoq')
            return

        if not self.to_user:
            await self.send_error('userni kiriting')
            return

        if not self.to_user:
            await self.send_error('bunday odam yoqku')
            return

        msg = await self.save_msg(self.from_user.id, self.to_user.id, msg)
        created_at = datetime.strftime(msg.created_at, self.__format_data)

        await self.channel_layer.group_send(
            self.groups, {
                'type': 'send_msg',
                'msg': msg.message,
                'to_user': msg.receiver_id,
                'from_user': msg.sender_id,
                'msg_id': msg.id,
                'created_at': created_at
            }
        )

    @database_sync_to_async
    def user_read_msg_db(self, user_id: int, msg_id: int):
        message = Message.objects.filter(receiver_id=user_id, id=msg_id).first()
        if message:
            message.is_read = True
            return message.sender_id, True
        return None, False

    async def read_msg(self, data):
        msg_id = data.get('msg_id')
        return await self.user_read_msg_db(self.from_user.id, msg_id)

    async def receive_json(self, data, *args):
        user_id = data.get('user_id')
        _type = data.get('type')
        self.to_user = await self.get_user(user_id)
        validator = {
            'msg': ('msg', 'user_id'),
            'read_msg': ('msg_id',)
        }
        if set(validator.get(_type, ())).difference(set(data.keys())):
            await self.send_error('Invalid data')

        if _type == 'msg':
            await self.msg_type(data)

        elif _type == 'read_msg':
            sender_id, is_read = await self.read_msg(data)
            if is_read:
                await self.send_message(sender_id, self.from_user.id, data.get('msg_id'))

        else:
            await self.send_error('type ni kiriting')
            return

    @database_sync_to_async  # ✅
    def save_msg(self, from_user: int, to_user: int, msg: str):
        return Message.objects.create(sender_id=from_user, receiver_id=to_user, message=msg)

    @database_sync_to_async  # ✅
    def get_user(self, pk) -> bool:
        return User.objects.filter(pk=pk).first()

    async def notify_user_status(self, is_online: bool = True):
        await self.channel_layer.group_send(
            self.groups,
            {
                'type': 'chat_change_status',
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
    def my_chats(self, to_user, from_id):
        return Message.objects.filter(
            Q(receiver=to_user) & Q(sender=from_id) |
            Q(receiver=from_id) & Q(sender=to_user)
        )

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

    async def send_read_msg(self, event):
        from_user = event['from_user']
        if self.from_user.pk == event['to_user'] or self.from_user.pk == from_user:
            data = {
                'type': 'read_msg',
                'msg_id': event['msg_id'],
                'from': event['to_user'],
            }
            await self.send_json(data)

    async def send_msg(self, event):
        from_user = event['from_user']
        if self.from_user.pk == event['to_user'] or self.from_user.pk == from_user:
            data = {
                'id': event['msg_id'],
                'msg': event['msg'],
                'from': from_user,
                'created_at': event['created_at']
            }
            await self.send_json(data)


'''
front -> back
msg, read_msg

back -> front
status, msg, read_msg
'''
