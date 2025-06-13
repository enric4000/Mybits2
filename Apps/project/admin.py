from django.contrib import admin

from Apps.project.models import Project, Valoration

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")

@admin.register(Valoration)
class ValorationAdmin(admin.ModelAdmin):
    list_display = ("id", "score", "project", "admin")
    search_fields = ("id", "score", "project", "admin")