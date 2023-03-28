from django.contrib.auth.models import AbstractUser
from django.db.models import Model, ForeignKey, SET_NULL, DateTimeField, CharField, BooleanField


class Users(AbstractUser):
    is_online = BooleanField(default=False)
    last_activity = DateTimeField(auto_now=True)


class Message(Model):
    sender = ForeignKey('apps.Users', SET_NULL, 'sended_messages', null=True)
    receiver = ForeignKey('apps.Users', SET_NULL, 'received_messages', null=True)
    message = CharField(max_length=4096)
    is_read = BooleanField(default=False)

    edited_at = DateTimeField(auto_now_add=True)
    created_at = DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('-created_at',)
