from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import get_watermark


class Client(AbstractUser):
    CLIENT_GENDER = (
        ('М', 'Мужчина'),
        ('Ж', 'Женщина')
    )
    avatar = models.ImageField(upload_to="clients/", blank=False, null=True)
    gender = models.CharField(max_length=1, choices=CLIENT_GENDER)
    username = models.CharField('client_name', max_length=150, unique=True)
    first_name = models.TextField('first_name', max_length=30)
    last_name = models.TextField('last_name', max_length=150)
    password = models.TextField('password', max_length=150)
    email = models.EmailField('e-mail', max_length=254, unique=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(Client, self).save(*args, **kwargs)
        image_path = self.avatar.path
        get_watermark(image_path)


class Match(models.Model):
    follower = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Поклонник',
    )
    person = models.ForeignKey(
        Client, null=True,
        on_delete=models.CASCADE,
        related_name='followed',
        verbose_name='Персона',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['follower', 'person'],
            name='unique_match'
        )]
