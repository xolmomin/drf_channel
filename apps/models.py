from django.contrib.auth.models import AbstractUser
from django.db.models import (SET_NULL, BooleanField, CharField, DateTimeField,
                              ForeignKey, Model, FileField)


class User(AbstractUser):
    is_online = BooleanField(default=False)
    last_activity = DateTimeField(auto_now=True)


class Message(Model):
    sender = ForeignKey('apps.User', SET_NULL, 'sended_messages', null=True)
    receiver = ForeignKey('apps.User', SET_NULL, 'received_messages', null=True)
    message = CharField(max_length=4096)
    is_read = BooleanField(default=False)

    edited_at = DateTimeField(auto_now_add=True)
    created_at = DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('-created_at',)


class File(Model):
    name = CharField(max_length=255)
    file = FileField(upload_to='files/')
    created_at = DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('-created_at',)
