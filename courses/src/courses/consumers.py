import json
from channels.generic.websocket import WebsocketConsumer
from django.forms.models import model_to_dict


class ClientConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=self.scope['user'].username)

    def disconnect(self, close_code):
        pass

    def send_mark_to_student(self, mark):
        mark_dict = model_to_dict(mark)
        self.send(text_data=json.dumps(mark_dict))
