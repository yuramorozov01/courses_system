from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from ws_app.consts import WS_BASE_EVENT_KEY, WS_MARK_UPDATE_EVENT_KEY


class BaseEventConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.group_name = ''
        if self.scope['user'].is_authenticated:
            self.group_name = f"{self.Meta.event_key}_{self.scope['user'].username}"
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

    class Meta:
        event_key = WS_BASE_EVENT_KEY

    def base_event(self, event):
        self.send_json(content=event)


class MarkUpdateEventConsumer(BaseEventConsumer):
    class Meta:
        event_key = WS_MARK_UPDATE_EVENT_KEY

    def mark_update_event(self, event):
        self.send_json(content=event)
