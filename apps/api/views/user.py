import mimetypes
from django.conf import settings

import uuid
from http import HTTPStatus
from uuid import UUID
import hashlib

from django.db import transaction
from django.db.models import Prefetch, Subquery, OuterRef
from django.utils.translation import gettext as _

from apps.api.serializers.offer_chat import OfferChatSerializer
from apps.api.views.base import SecuredView
from apps.api.errors import ValidationException, ProblemDetailException
from apps.api.filters.user import UserFilter
from apps.api.forms.user import UserForm
from apps.api.response import SingleResponse, PaginationResponse
from django.http import FileResponse

from apps.core.models import OfferChat, Message
from apps.core.models.user import User
from apps.api.serializers.user import UserSerializer

from object_checker.base_object_checker import has_object_permission


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


class UserChat(SecuredView):

    def get(self, request, user_id: UUID):

        if not has_object_permission('check_user_chats', user=request.user, obj=user_id):
            raise ProblemDetailException(request, _('Permission denied.'), status=HTTPStatus.FORBIDDEN)

        last_message = Message.objects.filter(offer_chat=OuterRef('pk')).order_by('-created_at')

        if request.GET.get('owner'):
            offer_chats = OfferChat.objects.filter(chat_users__user_id=user_id, chat_users__owner=True). \
                annotate(last_message_id=Subquery(last_message.values('id')[:1])). \
                annotate(last_message_content=Subquery(last_message.values('content')[:1])). \
                annotate(last_message_user=Subquery(last_message.values('user__username')[:1])). \
                order_by('-updated_at')
        else:
            offer_chats = OfferChat.objects.filter(chat_users__user_id=user_id, chat_users__owner=False). \
                annotate(last_message_id=Subquery(last_message.values('id')[:1])). \
                annotate(last_message_content=Subquery(last_message.values('content')[:1])). \
                annotate(last_message_user=Subquery(last_message.values('user__username')[:1])). \
                order_by('-updated_at')

        return PaginationResponse(request, offer_chats, serializer=OfferChatSerializer.User)
