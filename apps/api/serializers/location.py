import datetime
from typing import List
from uuid import UUID

from porcupine.base import Serializer


class LocationSerializer:
    class Base(Serializer):
        longitude: str
        latitude: str
