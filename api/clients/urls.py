from django.urls import path

from clients.views import ClientCreate, ClientList

urlpatterns = [
    path('clients/create/', ClientCreate.as_view()),
    path('list/', ClientList.as_view()),
]
