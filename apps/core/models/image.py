from django.db import models
from apps.core.models.base import BaseModel, private_storage
from django.utils.translation import gettext as _


class Image(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'images'
        default_permissions = ()

    class MimeType(models.TextChoices):
        JPEG = 'image/jpeg'
        PNG = 'image/png'

    def _upload_to_path(self, filename):

        return f"images/offers/{self.offer_id}/{filename}"

    path = models.FileField(
        null=False,
        max_length=255,
        verbose_name=_('image_path'),
        upload_to=_upload_to_path,
        storage=private_storage
    )
    mime_type = models.CharField(
        db_column='mime_type',
        max_length=20,
        choices=MimeType.choices,
    )

    offer = models.ForeignKey('Offer', null=True, on_delete=models.CASCADE, related_name='images',
                             verbose_name=_('image_offer'))

