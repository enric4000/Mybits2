from django.contrib import admin

from Apps.warehouse.models import Luggage, Warehouse

# Register your models here.
@admin.register(Warehouse)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")

@admin.register(Luggage)
class LuggageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("id", "name")
