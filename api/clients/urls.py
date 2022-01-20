from django.urls import path

from clients.views import ClientCreate, MatchCreateDelete

urlpatterns = [
    path('clients/create/', ClientCreate.as_view()),
    path('clients/<int:person_id>/match/', MatchCreateDelete.as_view()),
]
