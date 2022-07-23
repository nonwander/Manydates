from django.urls import path

from api.about.views import AboutAuthorView, AboutTechView

app_name = 'api.about'

urlpatterns = [
    path('author/', AboutAuthorView.as_view(), name='author'),
    path('tech/', AboutTechView.as_view(), name='tech'),
]
