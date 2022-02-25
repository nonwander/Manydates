from django.conf import settings
from django.conf.urls.static import static

from debug_toolbar import urls as debug_toolbar

from .urls import *

third_party_patterns += (
    path('__debug__/', include(debug_toolbar)),
)

django_patterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
django_patterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

urlpatterns += django_patterns + third_party_patterns
