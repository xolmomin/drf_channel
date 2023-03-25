import os
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from apps import routing
from apps.utils.jwt_auth_middleware_stack import JWTAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # 'http': django_asgi_app,
    'websocket': JWTAuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
})
