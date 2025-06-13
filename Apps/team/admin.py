from django.contrib import admin
from Apps.team.models import Team


# Register your models here.
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")
