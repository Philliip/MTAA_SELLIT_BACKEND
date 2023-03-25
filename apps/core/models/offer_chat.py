from django.db import models
from apps.core.models.base import BaseModel


class OfferChat(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'offers_chats'
        default_permissions = ()

    offer = models.ForeignKey('Offer', null=False, related_name='chats', on_delete=models.CASCADE)

