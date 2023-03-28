from django.db import models
from apps.core.models.base import BaseModel


class OfferChatUser(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'offers_chats_users'
        default_permissions = ()

    offer_chat = models.ForeignKey('OfferChat', null=False, related_name='chat_users', on_delete=models.CASCADE)
    user = models.ForeignKey('User', null=False, related_name='offer_chat_users', on_delete=models.CASCADE)
    owner = models.BooleanField(default=False, null=False)

