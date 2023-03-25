from uuid import UUID

from porcupine.base import Serializer

from apps.api.serializers.offer_chat import OfferChatSerializer
from apps.api.serializers.user import UserSerializer


class OfferChatUserSerializer:
    class Base(Serializer):
        id: UUID
        offer_chat = OfferChatSerializer.Base
        user: UserSerializer.Base
        owner: bool


