from django.forms import fields
from django_api_forms import Form, EnumField
from apps.core.models import ApiKey


class ApiKeyForm:
    class Base(Form):
        secret = fields.CharField(required=True, max_length=100)
        name = fields.CharField(required=True, max_length=100)
        platform = EnumField(enum=ApiKey.DevicePlatform, required=True)

    class Update(Form):
        secret = fields.CharField(required=False, max_length=100)
        name = fields.CharField(required=False, max_length=100)
        platform = EnumField(enum=ApiKey.DevicePlatform, required=False)
        is_active = fields.BooleanField(required=False)
