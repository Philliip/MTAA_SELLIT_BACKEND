from uuid import UUID

from apps.api.filters.city import CityFilter
from apps.api.serializers.city import CitySerializer
from apps.api.views.base import SecuredView
from http import HTTPStatus
from django.db import transaction
from django.utils.translation import gettext as _
from apps.api.errors import ValidationException, ProblemDetailException
from apps.api.forms.city import CityForm
from apps.core.models.city import City
from apps.api.response import SingleResponse, PaginationResponse


class CityManagement(SecuredView):

    @transaction.atomic()
    def post(self, request):
        form = CityForm.Create.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        city = City()
        form.populate(city)
        city.save()

        return SingleResponse(request, city, serializer=CitySerializer.Base, status=HTTPStatus.CREATED)

    def get(self, request):
        cities = CityFilter(request.GET, queryset=City.objects.all(), request=request).qs

        return PaginationResponse(request, cities, serializer=CitySerializer.Base)


class CityDetail(SecuredView):
    @staticmethod
    def _get_city(request, city_id: UUID) -> City:
        try:
            city = City.objects.get(pk=city_id)
        except City.DoesNotExist as e:
            raise ProblemDetailException(request, _("City not found"), status=HTTPStatus.NOT_FOUND, previous=e)

        return city

    def get(self, request, city_id: UUID):
        city = self._get_city(request, city_id)

        return SingleResponse(request, city, serializer=CitySerializer.Base)

    @transaction.atomic
    def put(self, request, city_id: UUID):
        form = CityForm.Update.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        city = self._get_city(request, city_id)

        form.populate(city)

        city.save()

        return SingleResponse(request, city, serializer=CitySerializer.Base)

    @transaction.atomic
    def delete(self, request, city_id: UUID):
        city = self._get_city(request, city_id)
        city.delete()

        return SingleResponse(request)
