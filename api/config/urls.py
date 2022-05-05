from django.conf import settings
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from . import views

handler404 = 'config.views.page_not_found'
handler500 = 'config.views.server_error'

local_patterns = [
    re_path(r'^favicon\.ico$', RedirectView.as_view(
        url=settings.STATIC_URL + 'img/favicon.ico', permanent=True
    )),
    path('', views.index, name='index'),
    path('500/', views.server_error, name='error500'),
    path('admin/', admin.site.urls),
    path('api/', include('clients.urls')),
    path('about/', include('about.urls', namespace='about')),
    path('404/', views.page_not_found, name='error404'),
]

django_patterns = [
]

django_patterns = [
]

third_party_patterns = [
]

urlpatterns = local_patterns + django_patterns + third_party_patterns
