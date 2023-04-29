import mimetypes
import uuid
import json

from apps.api.serializers.expo_token import ExpoTokenSerializer
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
        data = json.loads(request.body.decode('utf-8'))
        expo_push_token = data.get('expotoken')

        try:
            expo_token = ExpoToken.objects.get(token__iexact=expo_push_token).first()
            expo_token.user = request.user
        except ExpoToken.DoesNotExist:

            form = ExpoForm.Create.create_from_request(request)

            if not form.is_valid():
                raise ValidationException(request, form)

            expo_token = ExpoToken()
            form.populate(expo_token)
            expo_token.user = request.user

        expo_token.save()

        return SingleResponse(request, expo_token, serializer=ExpoTokenSerializer.Base, status=HTTPStatus.CREATED)
