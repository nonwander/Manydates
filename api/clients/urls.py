from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page


from clients.views import ClientCreate, ClientList, MatchCreateDelete

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

urlpatterns = [
    path('clients/', ClientCreate.as_view()),
    path('clients/<int:person_id>/match/', MatchCreateDelete.as_view()),
    path('clients/list/', cache_page(CACHE_TTL)(ClientList.as_view())),
]
