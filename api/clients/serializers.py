from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from .models import Client, Match


class ClientSerializer(serializers.ModelSerializer):
    is_match = serializers.SerializerMethodField()
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=Client.objects.all()
        )]
    )

    class Meta:
        fields = [
            'email', 'id', 'username', 'first_name',
            'last_name', 'avatar', 'gender', 'is_match'
        ]
        model = Client

    def get_is_match(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        if Match.objects.filter(person=obj, follower=user).exists():
            return True
        return False


class ClientMatchSerializer(serializers.ModelSerializer):
    queryset = Client.objects.all()

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
            raise serializers.ValidationError('Вы не можете отметить себя самого.')
        return data
