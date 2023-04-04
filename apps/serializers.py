from django.contrib.auth.hashers import make_password

from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from apps.models import Message, User, File


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_online')


class MessageModelSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'message', 'is_read', 'sender', 'receiver', 'created_at')


class UserCreateModelSerializer(ModelSerializer):
    confirm_password = CharField(max_length=255, read_only=True)

    def validate(self, data: dict):
        data['password'] = make_password(data['password'])
        return data

    class Meta:
        model = User
        fields = ('first_name', 'username', 'password', 'confirm_password')


class MyMessageListModelSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'message', 'is_read', 'sender', 'receiver', 'created_at')


class FileUploadModelSerializer(ModelSerializer):
    class Meta:
        model = File
        exclude = ()


class FileGetModelSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
