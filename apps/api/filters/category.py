import django_filters

from apps.core.models.category import Category


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')


    class Meta:
        model = Category
        fields = []
