import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from ws_app.middleware import JWTAuthMiddlewareStack
from ws_app.routings import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courses.settings')

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': JWTAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
