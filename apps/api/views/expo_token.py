import mimetypes
import uuid

from apps.api.views.base import SecuredView
from http import HTTPStatus
from django.db import transaction

from apps.api.errors import ValidationException
from apps.api.forms.expo_token import ExpoForm
from apps.api.response import SingleResponse
from apps.core.models import ExpoToken


class ExpoTokenManagement(SecuredView):

    @transaction.atomic
    def post(self, request):
        expo_push_token = request.POST.get('expotoken')

        expo_token = ExpoToken.objects.filter(token__iexact=expo_push_token).first()

        if expo_token:
            expo_token.user = request.user

        else:
            form = ExpoForm.Create.create_from_request(request)

            if not form.is_valid():
                raise ValidationException(request, form)

            expo_token = ExpoToken()
            form.populate(expo_token)
            expo_token.user = request.user

        expo_token.save()

        return SingleResponse(request, status=HTTPStatus.CREATED)
