from rest_framework.serializers import ModelSerializer

from apps.models import Users, Message


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'username', 'is_online')


class MessageModelSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'message', 'is_read', 'sender', 'receiver', 'created_at')
