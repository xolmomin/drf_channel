from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.models import Message, User, File
from apps.serializers import (MessageModelSerializer, UserCreateModelSerializer, UserModelSerializer,
                              FileUploadModelSerializer, FileGetModelSerializer)


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateModelSerializer


class MyChatListApiView(ListAPIView):
    queryset = User.objects.all()
    filter_backends = None
    permission_classes = (IsAuthenticated,)
    serializer_class = UserModelSerializer


class ChatMessageListApiView(ListAPIView):
    '''
    userga tegishli barcha xabarlarni olish
    '''
    queryset = Message.objects.all()
    filter_backends = None
    permission_classes = (IsAuthenticated,)
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


class UploadFileView(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileUploadModelSerializer
    parser_classes = (MultiPartParser,)
    pagination_class = None
    http_method_names = 'post', 'get'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FileGetModelSerializer
        return super().get_serializer_class()
