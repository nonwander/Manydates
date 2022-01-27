from django_filters import rest_framework as filters
from .models import Client
from .utils import get_clients_within_radius


class ClientListFilter(filters.FilterSet):
    gender = filters.filters.ChoiceFilter(
        choices=Client.CLIENT_GENDER,
        field_name='gender',
    )
    first_name = filters.CharFilter(lookup_expr='exact')
    last_name = filters.CharFilter(lookup_expr='exact')
    get_in_distance_km = filters.NumberFilter(method='filter')

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Client
        fields = ['gender', 'first_name', 'last_name', 'get_in_distance_km']

    def filter(self, request, queryset, value):
        latitude = self.user.latitude
        longitude = self.user.longitude
        value = float(value)
        func_in_raw = get_clients_within_radius(latitude, longitude)
        queryset = Client.objects.all().annotate(
            distance=func_in_raw
        ).order_by('distance').exclude(username=self.user)
        queryset = queryset.filter(distance__lt=value)
        return queryset
