from typing import List
from uuid import UUID
import datetime

from porcupine.base import Serializer
from apps.api.serializers.image import ImageSerializer
from apps.api.serializers.user import UserSerializer

class OfferSerializer:
    class Base(Serializer):
        id: UUID
        title: str
        category_id: UUID
        city_id: UUID
        user_id: UUID
        price: float
        images: List[ImageSerializer.Base]
        views: int
        user: UserSerializer.Base

    class Detail(Base):
        description: str
        created_at: datetime.datetime

    class Chat(Serializer):
        id: UUID
        title: str
        price: float
        user: UserSerializer.Base


