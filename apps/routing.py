from django.urls import path

from apps import consumers

websocket_urlpatterns = [
    path(r'ws/<int:room_name>', consumers.ChatConsumer.as_asgi()),
]
