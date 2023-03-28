import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from apps.core.models import Token, Message, OfferChatUser, OfferChat


class OfferChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.offer_chat_id = self.scope['url_route']['kwargs']['offer_chat_id']
        self.user = await self.authenticate_user(self.scope['headers'])
        self.last_message = None

        if self.user:
            # Join activity group
            await self.channel_layer.group_add(
                self.offer_chat_id,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

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

        message_obj = await self.save_message(self.user, self.offer_chat_id, message)

        # Send message to activity group
        await self.channel_layer.group_send(
            self.offer_chat_id, {'type': 'chat_message',
                                 'message': message,
                                 "username": self.user.username,
                                 "created_at": message_obj.created_at.strftime("%Y-%m-%d %H:%M:%S")}
        )

    @database_sync_to_async
    def save_message(self, user, offer_chat_id, content):
        message = Message.objects.create(user=user, offer_chat_id=offer_chat_id, content=content)
        OfferChat.objects.filter(id=offer_chat_id).update(updated_at=timezone.now())
        return message

    # Receive message from activity group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        created_at = event['created_at']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"username": username, "message": message, "created_at": created_at}))

    @database_sync_to_async
    def check_user(self, token_key):

        try:
            token = Token.objects.get(pk=token_key)

        except Token.DoesNotExist:
            return None

        if not OfferChatUser.objects.filter(offer_chat_id=self.offer_chat_id, user=token.user).exists():
            return None

        return token.user

    async def authenticate_user(self, headers):
        headers_dict = dict(headers)
        auth_header = headers_dict.get(b'authorization')

        if auth_header:
            token_key = auth_header.decode().split(" ")[1]
            user = await self.check_user(token_key)
            return user

        return None
