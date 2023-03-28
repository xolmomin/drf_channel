from django.urls import path

from apps import consumers

websocket_urlpatterns = [
    path('ws', consumers.ChatConsumer.as_asgi()),
]
