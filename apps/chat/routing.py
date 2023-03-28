# chat/routing.py
from django.urls import re_path

from apps.chat.consumers import chat

websocket_urlpatterns = [
    re_path(r'(?P<offer_chat_id>[\w-]+)/chat/$', chat.OfferChatConsumer.as_asgi()),
]
