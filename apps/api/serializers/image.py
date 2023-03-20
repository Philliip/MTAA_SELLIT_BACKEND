import urllib.parse
from uuid import UUID

from porcupine.base import Serializer
from apps.core.models import Image
from django.conf import settings


class ImageSerializer:
    class Base(Serializer):
        id: UUID
        url: str

        @staticmethod
        def resolve_url(data: Image, **kwargs) -> str:
            return urllib.parse.urljoin(settings.BASE_URL, f"images/{str(data.id)}")
