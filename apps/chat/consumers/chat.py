import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async


from django.utils import timezone
import requests

from apps.core.models import Token, Message, OfferChatUser, OfferChat, Location, ExpoToken

@sync_to_async
def send_push_notification(token, title, body):
    url = 'https://exp.host/--/api/v2/push/send'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'to': token,
        'title': title,
        'body': body,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return True
    else:
        print(f"Failed to send push notification: {response.text}")
        return False


class OfferChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.offer_chat_id = self.scope['url_route']['kwargs']['offer_chat_id']
        self.last_message = None

        await self.channel_layer.group_add(
            self.offer_chat_id,
            self.channel_name
        )

        await self.accept()

    # Leave activity chat
    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.offer_chat_id,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        location = text_data_json['location']
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        username = text_data_json['username']

        message_obj = await self.save_message(user_id, self.offer_chat_id, content=message, location=location)

        title = f"New message from {username}"
        body = message

        expo_tokens = await self.get_expo_tokens(user_id)
        for expo_token in expo_tokens:
            await send_push_notification(expo_token, title, body)

        # Send message to activity group
        await self.channel_layer.group_send(
            self.offer_chat_id, {'type': 'chat_message',
                                 "user_id": user_id,
                                 'message': message,
                                 "username": username,
                                 "created_at": message_obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                 "location": location}
        )

    @database_sync_to_async
    def save_message(self, user_id, offer_chat_id, content=None, location=None):
        location_obj = None
        if location:
            longitude = content.split(':')[0]
            latitude = content.split(':')[1]
            location_obj = Location.objects.create(longitude=longitude, latitude=latitude)

        message = Message.objects.create(user_id=user_id, offer_chat_id=offer_chat_id, content=content,
                                         location=location_obj)
        OfferChat.objects.filter(id=offer_chat_id).update(updated_at=timezone.now())
        return message

    @database_sync_to_async
    def get_expo_tokens(self, user_id):
        expo_tokens = ExpoToken.objects.filter(user_id=user_id)
        return expo_tokens

    # Receive message from activity group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        created_at = event['created_at']
        location = event['location']
        user_id = event['user_id']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"username": username, "message": message, "created_at": created_at,
                                              "location": location, "user_id": user_id}))


