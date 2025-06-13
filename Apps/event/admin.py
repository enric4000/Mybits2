from django.contrib import admin
from Apps.event.models import Event


# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "AppName")
    search_fields = ("id", "name", "AppName")
