from django.db import models
from apps.core.models.base import BaseModel
from django.utils.translation import gettext as _


class Message(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'messages'
        default_permissions = ()

    user = models.ForeignKey('User', null=False, related_name='messages', on_delete=models.CASCADE)
    offer_chat = models.ForeignKey('OfferChat', null=False, related_name='messages', on_delete=models.CASCADE)
    content = models.CharField(max_length=200, null=True, verbose_name=_('message_content'))
    location = models.ForeignKey('Location', null=True, related_name='messages', on_delete=models.CASCADE)
