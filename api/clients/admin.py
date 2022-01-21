from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Client


class ClientsAdmin(UserAdmin):
    list_display = (
        'avatar', 'username', 'password',
        'gender', 'first_name', 'last_name', 'email'
    )
    empty_value_display = "-пусто-"


admin.site.register(Client, ClientsAdmin)
