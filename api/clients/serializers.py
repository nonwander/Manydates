from django.contrib.auth.hashers import make_password
from django.contrib.gis.geos import Point

from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .models import Client, Match


class ClientSerializer(serializers.ModelSerializer):
    """Сериализация полей модели клиента.
    Версия API 1.0 позволяет использовать два поля для отображения и записи
    геоданных. Формат JSON иеет вид:
    "longitude": 0.0,
    "latitude": 0.0
    ДОБАВЛЕНО: можно использовать также одно поле типа Point, как в версии 2.0.
    """
    is_match = serializers.SerializerMethodField()
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=Client.objects.all()
        )]
    )

    class Meta:
        fields = [
            'id', 'username', 'email', 'first_name', 'password',
            'last_name', 'avatar', 'gender', 'is_match'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
        model = Client

    def to_internal_value(self, data):
        request = self.context.get('request')
        if request.version is None:
            if hasattr(data, 'longitude') and hasattr(data, 'latitude'):
                x = float(data['longitude'])
                y = float(data['latitude'])
                location = Point(x, y)
                data['location'] = location
        return super().to_internal_value(data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request.version is None:
            representation['longitude'] = instance.longitude
            representation['latitude'] = instance.latitude
            representation.pop('location')
        return representation

    def get_is_match(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        if obj.is_followed:
            return True
        return False

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(ClientSerializer, self).create(validated_data)


class ClientSerializerVer2(ClientSerializer):
    """Сериализация полей модели клиента API v2.0.
    Для геоданных используется только одно поле типа Point.
    Формат JSON-представления:
    "location": {
            "type": "Point",
            "coordinates": [
                0.0,
                0.0
            ]
    }
    ДОБАВЛЕНО: в версии 1.0 предусмотрено использование обоих представлений.
    """
    location = PointField()

    ClientSerializer.Meta.fields += [
        'location'
    ]


class ClientMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = [
            'follower', 'person'
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Match.objects.all(),
                fields=['follower', 'person'],
                message=('Вы уже отметили этого человека.')
            )
        ]

    def validate(self, data):
        person = data.get('person')
        follower = self.context['request'].user
        if follower == person:
            message = 'Вы не можете отметить себя самого.'
            raise serializers.ValidationError(message)
        return data
