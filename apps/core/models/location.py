from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models.base import BaseModel


class Location(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'locations'
        default_permissions = ()

    longitude = models.CharField(max_length=255, null=False, verbose_name=_('location_message'))
    latitude = models.CharField(max_length=255, null=False, verbose_name=_('coordinates_message'))
