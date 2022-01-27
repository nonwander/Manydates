from django.conf import settings
from django.core.mail import send_mail
from django.db.models.expressions import RawSQL
import math
from django.db.backends.signals import connection_created
from django.dispatch import receiver


def send_mail_notify(client_1, client_2):
    site_service_email = settings.EMAIL_HOST_USER
    message_follower = (
        'Вы понравились {}! Почта участника: {}').format(
            client_2.get_full_name(), client_2.email
    )
    message_person = (
        'Вы понравились {}! Почта участника: {}').format(
            client_1.get_full_name(), client_1.email
    )
    send_mail('Тема', message_follower, site_service_email, [client_1.email])
    send_mail('Тема', message_person, site_service_email, [client_2.email])


def get_clients_within_radius(latitude, longitude):
    """Функция для определения дистанции между участниками.
    Функция вычисляет кратчайшее расстояние между двумя точками на поверхности
    сферы, измеренное вдоль поверхности сферы. Используется понятие:
    "Расстояние большого круга, ортодромное расстояние."
    Источник: https://en.wikipedia.org/wiki/Great-circle_distance
    """
    # MEAN_EARTH_RADIUS_KM = 6371
    gcd_formula = "6371 * acos(least(greatest(\
    cos(radians(%s)) * cos(radians(latitude)) \
    * cos(radians(longitude) - radians(%s)) + \
    sin(radians(%s)) * sin(radians(latitude)) \
    , -1), 1))"
    distance_raw_sql = RawSQL(
        gcd_formula,
        (latitude, longitude, latitude)
    )
    return distance_raw_sql


@receiver(connection_created)
def extend_sqlite(connection=None, **kwargs):
    """Функция добавляет используемые в вычислениях функции gcd_formula
    математические функции для sqlite.
    """
    if connection.vendor == "sqlite":
        cf = connection.connection.create_function
        cf('acos', 1, math.acos)
        cf('cos', 1, math.cos)
        cf('radians', 1, math.radians)
        cf('sin', 1, math.sin)
        cf('least', 2, min)
        cf('greatest', 2, max)
