from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from apps.views import MyChatListApiView, ChatMessageListApiView, UserCreateAPIView, MyMessageListAPIView

urlpatterns = (
    path('register', UserCreateAPIView.as_view(), name='register'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('my-chat-list', MyChatListApiView.as_view(), name='my_chat_list'),
    path('messages/<int:user_id>', ChatMessageListApiView.as_view(), name='messages'),
    path('my-message-list', MyMessageListAPIView.as_view(), name='my_message')
)
