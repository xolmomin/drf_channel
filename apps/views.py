from django.db.models import Q
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response

from apps.models import Users, Message
from apps.serializers import UserModelSerializer, MessageModelSerializer


class MyChatListApiView(ListAPIView):
    queryset = Users.objects.all()
    filter_backends = None
    serializer_class = UserModelSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ChatMessageListApiView(ListAPIView):
    '''
    userga tegishli barcha xabarlarni olish

    '''
    queryset = Message.objects.all()
    filter_backends = None
    serializer_class = MessageModelSerializer

    def list(self, request, *args, **kwargs):
        user_id_1 = request.user.id
        user_id_2 = kwargs.get('user_id')
        queryset = Message.objects.filter(
            Q(sender_id=user_id_1) & Q(receiver_id=user_id_2) |
            Q(sender_id=user_id_2) & Q(receiver_id=user_id_1)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
