from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .filters import ClientListFilter
from .models import Client, Match
from .serializers import ClientSerializer, ClientMatchSerializer
from .utils import send_mail_notify


class ClientCreate(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_class = ClientListFilter


class MatchCreateDelete(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def check_match(self, follower, person):
        """Метод проверяет наличие взаимных отметок участников
        и в положительном случае вызывает функцию send_mail_notify
        для формирования email-уведомлений обоим участникам.
        """
        is_user_follower_to_person = Match.objects.filter(
            person=person, follower=follower
        ).exists()
        is_person_follower_to_user = Match.objects.filter(
            person=follower, follower=person
        ).exists()
        is_match_both_users = (
            is_user_follower_to_person and is_person_follower_to_user
        )
        if is_match_both_users:
            send_mail_notify(follower, person)

    def get(self, request, person_id):
        follower = request.user
        person = get_object_or_404(Client, id=person_id)
        data = {
            'follower': follower.id,
            'person': person_id
        }
        serializer = ClientMatchSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.check_match(follower, person)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, person_id):
        follower = request.user
        person = get_object_or_404(Client, id=person_id)
        obj = get_object_or_404(Match, follower=follower, person=person)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
