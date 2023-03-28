from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from apps.views import MyChatListApiView, ChatMessageListApiView

urlpatterns = [
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('my-chat-list', MyChatListApiView.as_view()),
    path('messages/<int:user_id>', ChatMessageListApiView.as_view()),
]


# 10.10.3.184