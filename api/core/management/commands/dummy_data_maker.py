import random

from django.core.management.base import BaseCommand
from django.db import transaction

from clients.factories import ClientFactory, MatchFactory
from clients.models import Client, Match

# TODO: реализовать возможность задавать пользователем количество данных
# TODO: добавить флаг для создания админа
NUM_CLIENTS = 50
NUM_MATCHES = 30


class Command(BaseCommand):
    help = 'Generates dummy data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Starting DUMMY-DATA-MAKER')
        self.stdout.write('Deleting old data')
        models = [Client, Match]
        for model in models:
            model.objects.all().delete()
        self.stdout.write('Finished!')
        self.stdout.write('Creating new data')
        people = []
        for _ in range(NUM_CLIENTS):
            user = ClientFactory()
            people.append(user)
        matches = []
        for _ in range(NUM_MATCHES):
            follower = random.choice(people)
            person = random.choice(people)
            following = MatchFactory(follower=follower, person=person)
            matches.append(following)
        self.stdout.write('Finished!')
