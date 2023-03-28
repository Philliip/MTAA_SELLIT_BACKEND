from django.forms import fields
from django_api_forms import Form, FieldList, FormFieldList
from django import forms
from apps.core.models import Category, City, Image
import django_api_forms
from django.conf import settings
from apps.api.forms.image import ImageForm

class OfferForm:
    class Update(Form):
        title = forms.CharField(required=True, max_length=50)
        description = forms.CharField(required=True, max_length=255)
        price = forms.DecimalField(max_digits=5, decimal_places=2)
        city_id = forms.ModelChoiceField(queryset=City.objects.all(), required=True)
        category_id = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
        images = FormFieldList(form=ImageForm.Create, required=False)

    class Create(Update):
        pass
