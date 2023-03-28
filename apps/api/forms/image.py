from django.conf import settings

from django_api_forms import Form, FileField, EnumField, ImageField

from apps.core.models import Image


class ImageForm:
    class Update(Form):
        image = ImageField(
            max_length=settings.DATA_UPLOAD_MAX_MEMORY_SIZE,
            mime=Image.MimeType.values,
            required=True
        )

    class Create(Update):
        pass
