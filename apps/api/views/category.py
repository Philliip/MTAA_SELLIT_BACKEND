from uuid import UUID

from apps.api.filters.category import CategoryFilter
from apps.api.serializers.category import CategorySerializer
from apps.api.views.base import SecuredView
from http import HTTPStatus
from django.db import transaction
from django.utils.translation import gettext as _
from apps.api.errors import ValidationException, ProblemDetailException
from apps.api.forms.category import CategoryForm
from apps.core.models.category import Category
from apps.api.response import SingleResponse, PaginationResponse


class CategoryManagement(SecuredView):

    @transaction.atomic()
    def post(self, request):
        form = CategoryForm.Create.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        category = Category()
        form.populate(category)
        category.save()

        return SingleResponse(request, category, serializer=CategorySerializer.Base, status=HTTPStatus.CREATED)

    def get(self, request):
        categories = CategoryFilter(request.GET, queryset=Category.objects.all(), request=request).qs

        return PaginationResponse(request, categories, serializer=CategorySerializer.Base)


class CategoryDetail(SecuredView):
    @staticmethod
    def _get_category(request, category_id: UUID) -> Category:
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist as e:
            raise ProblemDetailException(request, _("City not found"), status=HTTPStatus.NOT_FOUND, previous=e)

        return category

    def get(self, request, category_id: UUID):
        category = self._get_category(request, category_id)

        return SingleResponse(request, category, serializer=CategorySerializer.Base)

    @transaction.atomic
    def put(self, request, category_id: UUID):
        form = CategoryForm.Update.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        category = self._get_category(request, category_id)

        form.populate(category)

        category.save()

        return SingleResponse(request, category, serializer=CategorySerializer.Base)

    @transaction.atomic
    def delete(self, request, category_id: UUID):
        category = self._get_category(request, category_id)
        category.delete()

        return SingleResponse(request)
