from django.forms import fields
from django_api_forms import Form


class CategoryForm:
    class Update(Form):
        name = fields.CharField(required=True, max_length=50)

    class Create(Update):
        pass
