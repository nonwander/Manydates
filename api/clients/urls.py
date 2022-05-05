from django.urls import path

from clients.views import ClientCreate, ClientList, MatchCreateDelete

urlpatterns = [
    path('clients/', ClientCreate.as_view()),
    path('clients/<int:person_id>/match/', MatchCreateDelete.as_view()),
    path('clients/list/', ClientList.as_view()),
]
