from django.urls import re_path

from courses import consumers

websocket_urlpatterns = [
    re_path(r'ws/$', consumers.ClientConsumer.as_asgi()),
]
