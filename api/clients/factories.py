import random

from django.contrib.gis.geos import Point

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from faker.providers import BaseProvider

from .models import Client, Match

CLIENT_GENDER = ['M', 'F', 'U']


class DjangoGeoPointProvider(BaseProvider):

    def geo_point(self, **kwargs):
        kwargs['coords_only'] = True
        faker = factory.faker.faker.Faker()
        coords = faker.local_latlng(**kwargs)
        return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)


class ClientFactory(DjangoModelFactory):
    factory.Faker.add_provider(DjangoGeoPointProvider)
    id = factory.Sequence(lambda n: n)
    gender = random.choice(list(Client.CLIENT_GENDER))[0]
    # TODO: реализовать загрузку изображений через внешний API по его URL
    avatar = factory.django.ImageField()
    username = factory.Sequence(
        lambda n: 'person_{}'.format(n + 1)
    )
    first_name = factory.Faker('first_name', locale='RU')
    last_name = factory.Faker('last_name', locale='RU')
    password = factory.LazyAttribute(
        lambda a: '{}_pass'.format(
            a.username
        ).lower()
    )
    email = factory.LazyAttribute(
        lambda a: '{}@fake.ry'.format(
            a.username
        ).lower()
    )
    location = factory.Faker('geo_point')

    class Meta:
        model = Client
        django_get_or_create = ('id', 'username', 'email')


class MatchFactory(DjangoModelFactory):
    follower = factory.SubFactory(ClientFactory)
    person = factory.SubFactory(ClientFactory)

    class Meta:
        model = Match
        django_get_or_create = ('follower', 'person')
