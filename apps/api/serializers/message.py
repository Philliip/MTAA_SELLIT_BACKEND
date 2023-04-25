import datetime
from typing import List
from uuid import UUID

from porcupine.base import Serializer

from apps.api.serializers.location import LocationSerializer
from apps.api.serializers.user import UserSerializer

class MessageSerializer:
    class Base(Serializer):
        id: UUID
        created_at: datetime.datetime
        content: str = None
        location: LocationSerializer.Base = None
        user: UserSerializer.Message
