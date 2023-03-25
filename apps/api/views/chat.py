import mimetypes
import uuid
from uuid import UUID
from django.db.models import F
from apps.api.filters.message import MessageFilter
from apps.api.serializers.message import MessageSerializer
from apps.api.serializers.offer_chat_user import OfferChatUserSerializer
from apps.api.views.base import SecuredView
from http import HTTPStatus
from django.db import transaction
from django.utils.translation import gettext as _
from apps.api.errors import ValidationException, ProblemDetailException
from apps.api.forms.offer import OfferForm
from apps.core.models import OfferChat, Offer, Image, OfferChatUsers, Message
from apps.api.response import SingleResponse, PaginationResponse

class ChatUser(SecuredView):
    def get(self, request, offer_chat_id: UUID):
        offer_chat_users = OfferChatUsers.objects.filter(offer_chat_id=offer_chat_id)

        return PaginationResponse(request, offer_chat_users, serializer=OfferChatUserSerializer.Base)

class ChatMessage(SecuredView):

    def get(self, request, offer_chat_id: UUID):

        timestamp = request.GET.get('timestamp', None)

        if timestamp:
            messages = MessageFilter(request.GET,
                                     queryset=Message.objects.filter(offer_chat_id=offer_chat_id,
                                                                     created_at__lt=timestamp).all(),
                                     request=request).qs
        else:
            messages = MessageFilter(request.GET,
                                     queryset=Message.objects.filter(offer_chat_id=offer_chat_id).all(),
                                     request=request).qs

        return PaginationResponse(request, messages, serializer=MessageSerializer.Base)

class ChatMessagesDetail(SecuredView):

    @staticmethod
    def _get_message(request, offer_chat_id: UUID, message_id: UUID) -> Message:
        try:
            message = Message.objects.get(id=message_id, offer_chat_id=offer_chat_id)

        except Message.DoesNotExist as e:
            raise ProblemDetailException(request, _("Message not found"), status=HTTPStatus.NOT_FOUND, previous=e)

        return message

    @transaction.atomic
    def delete(self, request, offer_chat_id: UUID, message_id: UUID):

        message = self._get_message(request, offer_chat_id, message_id)

        message.hard_delete()

        return SingleResponse(request)
