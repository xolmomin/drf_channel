from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from apps.views import (ChatMessageListApiView, MyChatListApiView, UserCreateAPIView, UploadFileView)

router = DefaultRouter()
router.register('file', UploadFileView, 'file')

urlpatterns = (
    path('register', UserCreateAPIView.as_view(), name='register'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('my-chat-list', MyChatListApiView.as_view(), name='my_chat_list'),
    path('messages/<int:user_id>', ChatMessageListApiView.as_view(), name='messages'),
    path('', include(router.urls))
)
