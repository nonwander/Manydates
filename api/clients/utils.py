from django.conf import settings
from django.core.mail import send_mail


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
