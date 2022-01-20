from django_filters import rest_framework as filters

from .models import Client


class ClientListFilter(filters.FilterSet):
    gender = filters.filters.ChoiceFilter(
        choices=Client.CLIENT_GENDER,
        field_name='gender',
    )
    first_name = filters.CharFilter(lookup_expr='exact')
    last_name = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Client
        fields = ['gender', 'first_name', 'last_name']
