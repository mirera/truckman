from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Client, Role, Preference

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Client)
admin.site.register(Role)
admin.site.register(Preference)