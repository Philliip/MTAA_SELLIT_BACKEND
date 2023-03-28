import datetime
from uuid import UUID

from porcupine.base import Serializer


class ApiKeySerializer:
    class Base(Serializer):
        id: UUID
        name: str
        platform: str
        is_active: bool
        created_at: datetime.datetime
