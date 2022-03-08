from django.contrib.gis.measure import Distance

from django_filters import rest_framework as filters

from .models import Client


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
    get_in_distance_km = filters.NumberFilter(method='geo_filter')

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Client
        fields = ['gender', 'first_name', 'last_name', 'get_in_distance_km']

    def geo_filter(self, queryset, name, value):
        user = self.user
        value = float(value)
        queryset = queryset.filter(
            location__distance_lt=(
                user.location,
                Distance(m=value)
            )
        )
        return queryset
