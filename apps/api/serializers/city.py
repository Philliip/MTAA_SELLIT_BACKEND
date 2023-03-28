from uuid import UUID

from porcupine.base import Serializer


class CitySerializer:
    class Base(Serializer):
        id: UUID
        name: str
        zip: str
