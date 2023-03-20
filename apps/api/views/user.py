import mimetypes
from django.conf import settings

import uuid
from http import HTTPStatus
from uuid import UUID
import hashlib

from django.db import transaction
from django.utils.translation import gettext as _

from apps.api.views.base import SecuredView
from apps.api.errors import ValidationException, ProblemDetailException
from apps.api.filters.user import UserFilter
from apps.api.forms.user import UserForm
from apps.api.response import SingleResponse, PaginationResponse
from django.http import FileResponse
from object_checker.base_object_checker import has_object_permission


from apps.core.models.user import User
from apps.api.serializers.user import UserSerializer


def _get_user(request, user_id: UUID) -> User:
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist as e:
        raise ProblemDetailException(request, _('User not found.'), status=HTTPStatus.NOT_FOUND, previous=e)

    return user


class UserManagement(SecuredView):
    EXEMPT_AUTH = ['POST']

    @transaction.atomic
    def post(self, request):
        form = UserForm.Create.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        password = form.cleaned_data['password']

        user = User()

        form.populate(user)
        user.hash = hashlib.sha256(user.id.bytes + user.email.encode()).hexdigest()
        user.set_password(password)
        user.save()

        return SingleResponse(request, user, serializer=UserSerializer.Detail, status=HTTPStatus.CREATED)

    def get(self, request):
        users = UserFilter(request.GET, queryset=User.objects.all(), request=request).qs

        return PaginationResponse(request, users, serializer=UserSerializer.Base)


class UserDetail(SecuredView):

    def get(self, request, user_id: UUID):
        user = _get_user(request, user_id)

        return SingleResponse(request, user, serializer=UserSerializer.Detail)

    @transaction.atomic
    def put(self, request, user_id: UUID):
        form = UserForm.Update.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        user = _get_user(request, user_id)
        if not has_object_permission('check_user', user=request.user, obj=user):
            raise ProblemDetailException(request, _('Permission denied.'), status=HTTPStatus.FORBIDDEN)

        if User.objects.filter(email=form.cleaned_data['email']).exclude(pk=user.id).exists():
            raise ProblemDetailException(
                request, _('User with the same email already exists.'), status=HTTPStatus.CONFLICT
            )

        form.populate(user)
        user.save()

        return SingleResponse(request, user, serializer=UserSerializer.Detail)

    @transaction.atomic
    def delete(self, request, user_id: UUID):
        user = _get_user(request, user_id)
        if not has_object_permission('check_user', user=request.user, obj=user):
            raise ProblemDetailException(request, _('Permission denied.'), status=HTTPStatus.FORBIDDEN)
        user.delete()

        return SingleResponse(request)


class UserMe(SecuredView):

    def get(self, request):
        return SingleResponse(request, request.user, serializer=UserSerializer.Me)


class UserProfileImage(SecuredView):

    def get(self, request, user_id: UUID):

        user = _get_user(request, user_id)

        return FileResponse(user.image, as_attachment=True, filename=user.image.name)

    @transaction.atomic
    def put(self, request, user_id: UUID):

        form = UserForm.Image.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        user = _get_user(request, user_id)

        if not has_object_permission('check_user', user=request.user, obj=user):
            raise ProblemDetailException(request, _('Permission denied.'), status=HTTPStatus.FORBIDDEN)

        user.image.save(name=f"{uuid.uuid4()}{mimetypes.guess_extension(form.cleaned_data['image'].content_type)}",
                        content=form.cleaned_data['image'])

        return SingleResponse(request, request.user, serializer=UserSerializer.Me)

    @transaction.atomic
    def delete(self, request, user_id: UUID):

        user = _get_user(request, user_id)
        if not has_object_permission('check_user', user=request.user, obj=user):
            raise ProblemDetailException(request, _('Permission denied.'), status=HTTPStatus.FORBIDDEN)

        if user.image.path == settings.DEFAULT_IMAGE:
            raise ProblemDetailException(
                request, _('You dont have a profile image.'), status=HTTPStatus.BAD_REQUEST
            )

        user.image.delete(save=False)
        user.image = settings.DEFAULT_IMAGE
        user.save()

        return SingleResponse(request)
