import django_filters

from apps.core.models.api_key import ApiKey


class ApiKeyFilter(django_filters.FilterSet):
    created_at_gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    platform = django_filters.MultipleChoiceFilter(choices=ApiKey.DevicePlatform.choices)

    class Meta:
        model = ApiKey
        fields = []
