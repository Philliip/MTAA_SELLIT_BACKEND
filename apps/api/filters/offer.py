import django_filters
from apps.core.models.offer import Offer


class OfferFilter(django_filters.FilterSet):
    views = django_filters.NumberFilter(field_name='views', lookup_expr="lte")
    city_id = django_filters.UUIDFilter()
    city = django_filters.CharFilter(field_name='city__name', lookup_expr='icontains')
    category_id = django_filters.UUIDFilter()
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    user_id = django_filters.UUIDFilter()

    created_at_gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = []
