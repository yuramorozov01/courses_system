import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from ws_app.consts import WS_MARK_UPDATE_EVENT_KEY


class EventConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = ''
        if self.scope['user'].is_authenticated:
            self.group_name = f"{WS_MARK_UPDATE_EVENT_KEY}_{self.scope['user'].username}"
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def mark_update_event(self, event):
        self.send(text_data=json.dumps(event))
