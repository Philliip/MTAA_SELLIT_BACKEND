import django_filters
from apps.core.models.message import Message


class MessageFilter(django_filters.FilterSet):
    user_id = django_filters.UUIDFilter()
    created_at_gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = []
