from uuid import UUID

from porcupine.base import Serializer


class CategorySerializer:
    class Base(Serializer):
        id: UUID
        name: str
