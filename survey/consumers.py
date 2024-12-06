import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Survey, Answer

class SurveyComsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.survey_id = self.scope['url_route']['kwargs']['survey_id']
        self.survey_group_name = f'survey_{self.survey_id}'

        await self.channel_layer.group_add(
            self.survey_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.survey_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.survey_group_name,
            {
                'type': 'survey_message',
                'message': message
            }
        )

    async def survey_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))