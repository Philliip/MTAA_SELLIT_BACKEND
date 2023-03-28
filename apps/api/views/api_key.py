from http import HTTPStatus
from uuid import UUID

from django.db import transaction
from django.utils.translation import gettext as _

from apps.api.errors import ValidationException, ProblemDetailException
from apps.api.filters.api_key import ApiKeyFilter
from apps.api.forms.api_key import ApiKeyForm
from apps.api.response import SingleResponse, PaginationResponse
from apps.api.serializers.api_key import ApiKeySerializer
from apps.api.views.base import SecuredView
from apps.core.models.api_key import ApiKey


class ApiKeyManagement(SecuredView):
    EXEMPT_AUTH = ["POST"]

    @transaction.atomic
    def post(self, request):
        form = ApiKeyForm.Base.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        api_key = ApiKey()
        form.populate(api_key)
        api_key.save()

        return SingleResponse(request, api_key, serializer=ApiKeySerializer.Base, status=HTTPStatus.CREATED)

    def get(self, request):
        api_keys = ApiKeyFilter(request.GET, queryset=ApiKey.objects.all(), request=request).qs

        return PaginationResponse(request, api_keys, serializer=ApiKeySerializer.Base)


class ApiKeyDetail(SecuredView):
    @staticmethod
    def _get_api_key(request, api_key_id: UUID) -> ApiKey:
        try:
            api_key = ApiKey.objects.get(pk=api_key_id)
        except ApiKey.DoesNotExist as e:
            raise ProblemDetailException(
                request, _("Api key not found"), status=HTTPStatus.NOT_FOUND, previous=e)

        return api_key

    def get(self, request, api_key_id: UUID):
        api_key = self._get_api_key(request, api_key_id)

        return SingleResponse(request, api_key, serializer=ApiKeySerializer.Base)

    @transaction.atomic
    def put(self, request, api_key_id: UUID):
        form = ApiKeyForm.Update.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        api_key = self._get_api_key(request, api_key_id)

        form.populate(api_key)
        api_key.save()

        return SingleResponse(request, api_key, serializer=ApiKeySerializer.Base)

    @transaction.atomic
    def delete(self, request, api_key_id: UUID):
        api_key = self._get_api_key(request, api_key_id)
        api_key.delete()

        return SingleResponse(request)
