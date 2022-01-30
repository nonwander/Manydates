import math

from django.conf import settings
from django.core.mail import send_mail
from django.db.backends.signals import connection_created
from django.db.models.expressions import RawSQL
from django.dispatch import receiver
from PIL import Image


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
    try:
        send_mail(
            'Тема',
            message_follower, site_service_email,
            [client_1.email]
        )
    except BaseException as err:
        err_message = f'{client_1.email} - {type(err)}'
        send_mail(
            'Ошибка отправки сообщения',
            err_message, site_service_email,
            [site_service_email]
        )
    try:
        send_mail(
            'Тема',
            message_person, site_service_email,
            [client_2.email]
        )
    except BaseException as err:
        err_message = f'{client_2.email} - {type(err)}'
        send_mail(
            'Ошибка отправки сообщения',
            err_message, site_service_email,
            [site_service_email]
        )


def set_watermark_full_filling(input_url):
    """Функция накладывет водяной знак на аватар пользователя.
    Внутри использует преобразование размера загруженного изображения
    под размер водяного знака.
    """
    position = (0, 0)
    image_url = str(input_url)
    watermark_url = settings.STATIC_WATERMARK
    watermark = Image.open(watermark_url)
    width, height = watermark.size
    input_image = Image.open(image_url)
    output_image = get_perfect_size_image(input_image, width, height)
    combined_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    combined_image.paste(output_image, (0, 0))
    combined_image.paste(watermark, position, mask=watermark)
    output_image = combined_image.convert('RGB')
    output_image.save(image_url)


def get_perfect_size_image(input_image, water_width, water_height):
    """Функция адаптирует изображение пользователя по размерам изображения
    водяного знака. Используется пропорциональное соотношение ширины и высоты.
    """
    img_width, img_height = input_image.size
    koef_water = water_width / water_height
    koef_img = img_width / img_height
    if koef_water == koef_img:
        input_image = input_image.resize(
            (water_width, water_height),
            Image.ANTIALIAS
        )
        return input_image
    elif koef_water > koef_img:
        new_img_height = img_height * koef_img
        delta = (img_height - new_img_height) // 2
        cropped = input_image.crop((0, delta, img_width, img_height - delta))
    elif koef_water < koef_img:
        new_img_width = img_width / koef_img
        delta = (img_width - new_img_width) // 2
        cropped = input_image.crop((delta, 0, img_width - delta, img_height))
    cropped = cropped.resize((water_width, water_height), Image.ANTIALIAS)
    return cropped


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
