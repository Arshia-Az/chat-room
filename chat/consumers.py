from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):


    def new_message(self, date):
        print(1111111)

    def fetch_message(self):
        pass


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    commands = {
        "new_message": new_message,
        "fetch_message": fetch_message,
    }

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(

            self.room_group_name,
            self.channel_name

        )

    def receive(self, text_data):
        text_data_dict = json.loads(text_data)
        message = text_data_dict['message']
        command = text_data_dict['command']


        self.commands[command](self, message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message

            }

        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))