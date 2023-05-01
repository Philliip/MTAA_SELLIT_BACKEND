from typing import List
from uuid import UUID

from porcupine.base import Serializer

from apps.api.serializers.message import MessageSerializer
from apps.api.serializers.offer import OfferSerializer


class OfferChatSerializer:
    class Base(Serializer):
        id: UUID
        offer: OfferSerializer.Chat

    class User(Base):
        last_message_id: UUID = None
        last_message_content: str = None
        last_message_user: str = None
        user_name: str = None
        user_image: str = None



