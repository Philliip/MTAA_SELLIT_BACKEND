from uuid import UUID

from porcupine.base import Serializer


class ExpoTokenSerializer:
    class Base(Serializer):
        id: UUID
        token: str
        user_id: UUID
