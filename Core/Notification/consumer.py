import json

from channels.generic.websocket import AsyncWebsocketConsumer



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

    async def send_photo_deletion(self, event):
        print('Я работаю')
        if self.scope['user'] in event['user_set_id']:
            await self.send(text_data=json.dumps({
                'notification': event['notification']
            }))



    async def send_global_event(self, event):
        notification = event['notification']
        await self.send(text_data=json.dumps({
            'notification': notification
        }))

