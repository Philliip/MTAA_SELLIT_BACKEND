from typing import List
from uuid import UUID

from porcupine.base import Serializer

from apps.api.serializers.image import ImageSerializer
from apps.api.serializers.offer import OfferSerializer


class OfferChatSerializer:
    class Base(Serializer):
        id: UUID
        offer: OfferSerializer.Chat

    class User(Base):
        last_message: ImageSerializer.Base = None



