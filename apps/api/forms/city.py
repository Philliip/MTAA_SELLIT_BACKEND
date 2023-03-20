from django.forms import fields
from django_api_forms import Form


class CityForm:
    class Update(Form):
        name = fields.CharField(required=True, max_length=50)
        zip = fields.CharField(required=True, max_length=10)

    class Create(Update):
        pass
