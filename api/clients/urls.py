from django.urls import path

from clients.views import ClientCreate

urlpatterns = [
    path('clients/create/', ClientCreate.as_view()),
]
