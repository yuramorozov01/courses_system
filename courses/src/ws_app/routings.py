from django.urls import path
from ws_app.consumers import MarkUpdateEventConsumer

websocket_urlpatterns = [
    path('ws/mark_update/', MarkUpdateEventConsumer.as_asgi()),
]
