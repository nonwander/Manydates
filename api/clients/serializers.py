from rest_framework import serializers, validators

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[validators.UniqueValidator(
            queryset=Client.objects.all()
        )]
    )

    class Meta:
        fields = [
            'email', 'id', 'username', 'first_name',
            'last_name', 'avatar', 'gender',
        ]
        model = Client
