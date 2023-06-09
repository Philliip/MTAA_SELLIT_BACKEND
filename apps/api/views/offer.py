import mimetypes
import uuid
import requests
from uuid import UUID
from django.db.models import F
from apps.api.filters.offer import OfferFilter
from apps.api.serializers.offer import OfferSerializer
from apps.api.serializers.offer_chat import OfferChatSerializer
from apps.api.views.base import SecuredView
from http import HTTPStatus
from django.db import transaction
from django.utils.translation import gettext as _
from apps.api.errors import ValidationException, ProblemDetailException
from apps.api.forms.offer import OfferForm
from apps.core.models import OfferChat, Offer, Image, OfferChatUser, ExpoToken
from apps.api.response import SingleResponse, PaginationResponse
from object_checker.base_object_checker import has_object_permission


class OfferManagement(SecuredView):
    EXEMPT_AUTH = ['GET']

    @transaction.atomic
    def post(self, request):

        form = OfferForm.Create.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        offer = Offer()
        form.populate(offer)
        offer.user = request.user
        offer.save()

        for image in form.cleaned_data.get('images', []):

            image_obj = Image.objects.create(
                mime_type=image['image'].content_type,
                offer_id=offer.pk,

            )

            image_obj.path.save(
                f"{uuid.uuid4()}{mimetypes.guess_extension(image['image'].content_type)}", image['image']
            )

        return SingleResponse(request, offer, serializer=OfferSerializer.Detail, status=HTTPStatus.CREATED)

    def get(self, request):

        offers = OfferFilter(request.GET, queryset=Offer.objects.all(), request=request).qs

        return PaginationResponse(request, offers, serializer=OfferSerializer.Base)


def _get_offer(request, offer_id: UUID) -> Offer:
    try:
        offer = Offer.objects.get(pk=offer_id)
    except Offer.DoesNotExist as e:
        raise ProblemDetailException(request, _("Offer not found"), status=HTTPStatus.NOT_FOUND, previous=e)
    return offer


class OfferDetail(SecuredView):
    EXEMPT_AUTH = ['GET']

    @transaction.atomic
    def get(self, request, offer_id: UUID):
        offer = _get_offer(request, offer_id)

        offer.views = F('views') + 1
        offer.save(update_fields=['views'])
        offer.refresh_from_db(fields=['views'])

        return SingleResponse(request, offer, serializer=OfferSerializer.Detail, status=HTTPStatus.OK)

    @transaction.atomic
    def put(self, request, offer_id: UUID):

        form = OfferForm.Update.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        offer = _get_offer(request, offer_id)

        if not has_object_permission('check_offer', user=request.user, obj=offer):
            raise ProblemDetailException(request, _('Permission denied.'), status=HTTPStatus.FORBIDDEN)

        form.populate(offer)

        offer.save()

        for image in form.cleaned_data.get('images', []):

            image_obj = Image.objects.create(
                mime_type=image['image'].content_type,
                offer_id=offer.pk,
            )

            image_obj.path.save(
                f"{uuid.uuid4()}{mimetypes.guess_extension(image['image'].content_type)}", image['image']
            )

        return SingleResponse(request, offer, serializer=OfferSerializer.Detail, status=HTTPStatus.OK)

    @transaction.atomic
    def delete(self, request, offer_id: UUID):
        offer = _get_offer(request, offer_id)

        if not has_object_permission('check_offer', user=request.user, obj=offer):
            raise ProblemDetailException(request, _('Permission denied.'), status=HTTPStatus.FORBIDDEN)

        images = offer.images.all()
        for image in images:
            image.path.delete()
        offer.hard_delete()

        return SingleResponse(request, status=HTTPStatus.NO_CONTENT)


class OfferChatManagement(SecuredView):

    def send_push_notification(self, token, title, body):
        url = 'https://exp.host/--/api/v2/push/send'
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'to': token,
            'title': title,
            'body': body,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return True
        else:
            print(f"Failed to send push notification: {response.text}")
            return False

    def get_expo_token_obj(self, user):
        return ExpoToken.objects.filter(user=user)

    @transaction.atomic
    def post(self, request, offer_id: UUID):

        offer = _get_offer(request, offer_id)

        try:
            offer_chat = OfferChat.objects.get(offer_id=offer_id, chat_users__user=request.user)
        except OfferChat.DoesNotExist:
            offer_chat = OfferChat.objects.create(offer_id=offer_id)
            OfferChatUser.objects.create(offer_chat=offer_chat, user=offer.user, owner=True)
            OfferChatUser.objects.create(offer_chat=offer_chat, user=request.user)

        expo_token_obj = self.get_expo_token_obj(offer.user)
        for token_obj in expo_token_obj:
            self.send_push_notification(token_obj.token, "New reaction", "Somebody reacted on your offer")

        return SingleResponse(request, offer_chat, serializer=OfferChatSerializer.Base, status=HTTPStatus.CREATED)
