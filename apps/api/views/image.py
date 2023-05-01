from uuid import UUID
from http import HTTPStatus
from django.db import transaction

from django.http import FileResponse
from django.utils.translation import gettext as _
from apps.api.errors import ProblemDetailException
from apps.core.models import Image
from apps.api.views.base import SecuredView
from apps.api.response import SingleResponse
from object_checker.base_object_checker import has_object_permission


class ImageDetail(SecuredView):
    EXEMPT_AUTH = ['GET']
    EXEMPT_API_KEY = ['GET']

    @staticmethod
    def _get_image(request, image_id: UUID) -> Image:

        try:
            image = Image.objects.get(pk=image_id)
        except Image.DoesNotExist:
            raise ProblemDetailException(request, _("Image not found"), status=HTTPStatus.NOT_FOUND)

        return image

    def get(self, request, image_id: UUID):

        image = self._get_image(request, image_id)

        return FileResponse(image.path)

    @transaction.atomic
    def delete(self, request, image_id: UUID):

        image = self._get_image(request, image_id)

        if not has_object_permission('check_delete', user=request.user, obj=image):
            raise ProblemDetailException(request, _('Permission denied.'), status=HTTPStatus.FORBIDDEN)

        image.path.delete()
        image.hard_delete()

        return SingleResponse(request, status=HTTPStatus.NO_CONTENT)
