from django.db import models
from apps.core.models.base import BaseModel
from django.utils.translation import gettext as _


class Offer(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'offers'
        default_permissions = ()

    title = models.CharField(max_length=200, null=False, verbose_name=_('offer_tittle'))
    description = models.CharField(max_length=255, null=False, verbose_name=_('offer_description'))
    price = models.DecimalField(null=False, max_digits=5, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, related_name='offers',
                                 verbose_name=_('offer_category'))

    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True, related_name='offers',
                             verbose_name=_('offer_city'))

    views = models.IntegerField(default=0, null=False)

    user = models.ForeignKey('User', on_delete=models.CASCADE, null=False, related_name='offers',
                             verbose_name=_('post_user'))
