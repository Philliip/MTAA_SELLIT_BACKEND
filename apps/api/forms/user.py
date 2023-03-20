from django.forms import fields
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django_api_forms import Form
import django_api_forms
from django import forms
from django.utils.translation import gettext as _

from apps.core.models import User, Image
from django.conf import settings


class UserForm:
    class Update(Form):

        name = fields.CharField(required=True, max_length=30)
        surname = fields.CharField(required=True, max_length=150)
        username = fields.CharField(required=True, max_length=150)
        email = fields.EmailField(required=True)

    class Create(Update):

        password = fields.CharField(required=True, validators=[validate_password])

        def clean_email(self):
            if User.all_objects.filter(email=self.cleaned_data['email']).exists():
                self.add_error(
                    ('email',),
                    ValidationError(_('User with the same email already exists.'), code='email-already-exists')
                )

            return self.cleaned_data['email']

        def clean_username(self):
            if User.all_objects.filter(username=self.cleaned_data['username']).exists():
                self.add_error(
                    ('username',),
                    ValidationError(_('User with the same username already exists.'), code='username-already-exists')
                )

            return self.cleaned_data['username']

    class Image(Form):
        image = django_api_forms.ImageField(max_length=settings.DATA_UPLOAD_MAX_MEMORY_SIZE,
                                            mime=Image.MimeType.values,
                                            required=True)
