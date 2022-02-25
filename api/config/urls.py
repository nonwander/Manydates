from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from . import views

local_patterns = [
    re_path(r'^favicon\.ico$', RedirectView.as_view(
        url=settings.STATIC_URL + 'img/favicon.ico', permanent=True
    )),
    path('admin/', admin.site.urls),
    path('api/', include('clients.urls')),
]

django_patterns = [
]

third_party_patterns = [
]

urlpatterns = local_patterns + django_patterns + third_party_patterns
