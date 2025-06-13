from django.contrib import admin

from Apps.hardware.models import HardwareItem

# Register your models here.
@admin.register(HardwareItem)
class HardwareItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "abreviation")
    search_fields = ("id", "name", "abreviation")
