from uuid import UUID
from datetime import datetime

from porcupine.base import Serializer


class UserSerializer:
    class Base(Serializer):
        id: UUID
        email: str
        name: str
        surname: str
        image_url: str

    class Detail(Base):
        last_login: datetime = None
        created_at: datetime

    class Me(Detail):
        pass

    class Message(Serializer):
        id: UUID
        username: str
        image_url: str
