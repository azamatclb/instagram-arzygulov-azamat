from django.contrib import admin

from apps.account.models import Profile


# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    list_display_link = ['username', 'email', 'first_name', 'last_name']


admin.site.register(Profile, ProfileAdmin)
