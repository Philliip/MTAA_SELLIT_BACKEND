import mimetypes
import uuid
from uuid import UUID
from django.db.models import F
from apps.api.filters.offer import OfferFilter
from apps.api.serializers.offer import OfferSerializer
from apps.api.views.base import SecuredView
from http import HTTPStatus
from django.db import transaction
from django.utils.translation import gettext as _
from apps.api.errors import ValidationException, ProblemDetailException
from apps.api.forms.offer import OfferForm
from apps.core.models.offer import Offer
from apps.core.models.image import Image
from apps.api.response import SingleResponse, PaginationResponse


class OfferManagement(SecuredView):

    @transaction.atomic
    def post(self, request):

        form = OfferForm.Create.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        offer = Offer()
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

        return SingleResponse(request, offer, serializer=OfferSerializer.Detail, status=HTTPStatus.CREATED)

    def get(self, request):

        offers = OfferFilter(request.GET, queryset=Offer.objects.all(), request=request).qs

        return PaginationResponse(request, offers, serializer=OfferSerializer.Base)

class OfferDetail(SecuredView):


    @staticmethod
    def _get_offer(request, offer_id: UUID) -> Offer:
        try:
            offer = Offer.objects.get(pk=offer_id)
        except Offer.DoesNotExist as e:
            raise ProblemDetailException(request, _("Offer not found"), status=HTTPStatus.NOT_FOUND, previous=e)
        return offer

    @transaction.atomic
    def get(self, request, offer_id: UUID):
        offer = self._get_offer(request, offer_id)

        offer.views = F('views') + 1
        offer.save(update_fields=['views'])
        offer.refresh_from_db(fields=['views'])

        return SingleResponse(request, offer, serializer=OfferSerializer.Detail)

    @transaction.atomic
    def put(self, request, offer_id: UUID):

        form = OfferForm.Update.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        offer = self._get_offer(request, offer_id)

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

        return SingleResponse(request, offer, serializer=OfferSerializer.Detail)

    @transaction.atomic
    def delete(self, request, offer_id: UUID):
        offer = self._get_offer(request, offer_id)

        images = offer.images.all()
        for image in images:
            image.path.delete()
        offer.hard_delete()

        return SingleResponse(request)
