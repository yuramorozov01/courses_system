from django.urls import path
from ws_app.consumers import EventConsumer

websocket_urlpatterns = [
    path('ws/mark_update/', EventConsumer.as_asgi()),
]
