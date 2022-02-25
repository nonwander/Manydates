from django.db.models import Prefetch

from django_filters import rest_framework as filters

from .models import Client, Match
from .utils import get_clients_within_radius


class CustomFilterBackend(filters.DjangoFilterBackend):

    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)
        if hasattr(view, 'get_filterset_kwargs'):
            kwargs.update(view.get_filterset_kwargs())
        return kwargs


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
        user = self.user
        latitude = user.latitude
        longitude = user.longitude
        value = float(value)
        func_in_raw = get_clients_within_radius(latitude, longitude)
        queryset = Client.objects.all().annotate(
            distance=func_in_raw
        ).order_by('distance').exclude(username=user).prefetch_related(
            Prefetch(
                'followed', queryset=Match.objects.filter(follower=user.id),
                to_attr='is_followed'
            )
        )
        queryset = queryset.filter(distance__lt=value)
        return queryset
