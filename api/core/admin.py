from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from clients.models import Client


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = (
            'avatar', 'username', 'password',
            'gender', 'first_name', 'last_name', 'email'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ClientsAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = (
        'avatar', 'username', 'email', 'password',
        'gender', 'first_name', 'last_name'
    )
    empty_value_display = "-пусто-"
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'gender', 'location')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password', 'avatar'),
        }),
    )


admin.site.register(Client, ClientsAdmin)
