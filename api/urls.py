from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from rest_framework import permissions

from .views import index, server_error, page_not_found, product

handler404 = 'api.views.page_not_found'
handler500 = 'api.views.server_error'

schema_view = get_schema_view(
   openapi.Info(
      title='Dating-Site API',
      default_version='v1',
      description='API documentation for Dating-Site',
      # TODO: terms_of_service='URL страницы с пользовательским соглашением',
      contact=openapi.Contact(email='servgram@mail.ru'),
      license=openapi.License(name='MIT License'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

local_patterns = [
    re_path(r'^favicon\.ico$', RedirectView.as_view(
        url=settings.STATIC_URL + 'img/favicon.ico', permanent=True
    )),
    path('', index, name='index'),
    path('500/', server_error, name='error500'),
    path('admin/', admin.site.urls),
    path('api/', include(
        ('api.clients.urls', 'api.clients'), namespace='clients')
    ),
    path('about/', include(
        ('api.about.urls', 'api.about'), namespace='about')
    ),
    path('product', product, name='product'),
    path('404/', page_not_found, name='error404'),
]

django_patterns = [
]

third_party_patterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', 
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), 
       name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), 
       name='schema-redoc'),
]

urlpatterns = local_patterns + django_patterns + third_party_patterns
