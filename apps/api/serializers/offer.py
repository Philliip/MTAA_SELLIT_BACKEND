from typing import List
from uuid import UUID
import datetime

from porcupine.base import Serializer
from apps.api.serializers.image import ImageSerializer

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

    class Detail(Base):
        description: str
        created_at: datetime.datetime

    class Chat(Serializer):
        id: UUID
        title: str
        price: float


