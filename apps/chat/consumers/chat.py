import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from apps.core.models import Token, Message, OfferChatUser, OfferChat


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
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        username = text_data_json['username']

        message_obj = await self.save_message(user_id, self.offer_chat_id, message)

        # Send message to activity group
        await self.channel_layer.group_send(
            self.offer_chat_id, {'type': 'chat_message',
                                 'message': message,
                                 "username": username,
                                 "created_at": message_obj.created_at.strftime("%Y-%m-%d %H:%M:%S")}
        )

    @database_sync_to_async
    def save_message(self, user_id, offer_chat_id, content):
        message = Message.objects.create(user_id=user_id, offer_chat_id=offer_chat_id, content=content)
        OfferChat.objects.filter(id=offer_chat_id).update(updated_at=timezone.now())
        return message

    # Receive message from activity group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        created_at = event['created_at']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"username": username, "message": message, "created_at": created_at}))


