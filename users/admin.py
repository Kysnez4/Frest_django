from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('id', 'email')
