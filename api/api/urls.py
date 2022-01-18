from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(
        url=settings.STATIC_URL + 'img/favicon.ico', permanent=True
    )),
    path('admin/', admin.site.urls),
    path('api/', include('clients.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
