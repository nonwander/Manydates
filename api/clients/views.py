from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ClientListFilter, CustomFilterBackend
from .models import Client, Match
from .serializers import (ClientMatchSerializer, ClientSerializer,
                          ClientSerializerVer2)
from .utils import send_mail_notify


class ClientCreate(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]


class ClientList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [CustomFilterBackend]
    filter_class = ClientListFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Client.objects.prefetch_related(
            Prefetch(
                'followed', queryset=Match.objects.filter(follower=user.id),
                to_attr='is_followed'
            )
        )
        return queryset

    def get_filterset_kwargs(self):
        return {
            'user': self.request.user,
        }

    def get_serializer_class(self):
        """Возвращает подходящий сериализатор
        на основе версии запросов REST API.
        """
        if self.request.version == '2.0':
            return ClientSerializerVer2
        return ClientSerializer


class MatchCreateDelete(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def check_match(self, current_user, person):
        """Метод проверяет наличие взаимных отметок участников
        и в положительном случае вызывает функцию send_mail_notify
        для формирования email-уведомлений обоим участникам.
        """
        is_person_follower_to_user = Match.objects.filter(
            person=current_user.id, follower=person['id']
        ).exists()
        if is_person_follower_to_user:
            send_mail_notify(current_user, person)

    def post(self, request, person_id):
        follower = request.user
        person = get_object_or_404(Client.objects.select_related().values(
            'id', 'username', 'email'
        ), id=person_id)
        data = {
            'follower': follower.id,
            'person': person['id']
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
