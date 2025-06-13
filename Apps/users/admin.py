from django.contrib import admin

from Apps.users.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "email")
    search_fields = ("id", "first_name", "email")
