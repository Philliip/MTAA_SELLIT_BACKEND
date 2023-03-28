import django_filters

from apps.core.models.city import City


class CityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    zip = django_filters.CharFilter(field_name='zip', lookup_expr='icontains')

    class Meta:
        model = City
        fields = []
