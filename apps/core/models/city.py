from django.db import models
from apps.core.models.base import BaseModel
from django.utils.translation import gettext as _


class City(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'cities'
        default_permissions = ()

    name = models.CharField(max_length=255, null=False, verbose_name=_('city_name'))
    zip = models.CharField(max_length=10, null=False, verbose_name=_('city_zip'))

