from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .filters import ClientListFilter
from .models import Client, Match
from .serializers import ClientSerializer, ClientMatchSerializer


class ClientCreate(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = ClientListFilter


class MatchCreateDelete(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, person_id):
        follower = request.user
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, person_id):
        follower = request.user
        person = get_object_or_404(Client, id=person_id)
        obj = get_object_or_404(Match, follower=follower, person=person)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
