import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.decorators import login_required


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_authenticated:
            await self.channel_layer.group_add('notification', self.channel_name)

            await self.accept()

        else:
            await self.close()



    async def send_notification_event(self, event):
        if event['user_photo_id'] == self.scope['user'].id:
            notification = event['notification']
            await self.send(text_data=json.dumps({
                'notification': notification
            }))

    async def send_global_event(self, event):
        notification = event['notification']
        await self.send(text_data=json.dumps({
            'notification': notification
        }))

