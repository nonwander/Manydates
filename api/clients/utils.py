from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail

from PIL import Image


def send_mail_notify(client_1, client_2):
    site_service_email = settings.EMAIL_HOST_USER
    message_follower = (
        f'Вы понравились {client_2["username"]}! ' +
        f'Почта участника: {client_2["email"]}'
    )
    message_person = (
        f'Вы понравились {client_1.username}! ' +
        f'Почта участника: {client_1.email}'
    )
    try:
        send_mail(
            'Взаимная симпатия!',
            message_follower, site_service_email,
            [client_1.email],
            fail_silently=False
        )
    except SMTPException as err:
        err_message = f'{client_1.email} - {type(err)}'
        send_mail(
            'Ошибка отправки сообщения',
            err_message, site_service_email,
            [site_service_email]
        )
    try:
        send_mail(
            'Взаимная симпатия!',
            message_person, site_service_email,
            [client_2['email']],
            fail_silently=False
        )
    except SMTPException as err:
        email = client_2['email']
        err_message = f'{email} - {type(err)}'
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
