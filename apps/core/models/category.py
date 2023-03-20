from django.db import models
from apps.core.models.base import BaseModel
from django.utils.translation import gettext as _


class Category(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'categories'
        default_permissions = ()

    name = models.CharField(max_length=255, null=False, verbose_name=_('category_name'))
