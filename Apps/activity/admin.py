from django.contrib import admin
from Apps.activity.models import Activity


# Register your models here.
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "start_date", "end_date")
    search_fields = ("id", "name", "type")
    list_filter = ("type", "start_date", "end_date")
    ordering = ("-start_date",)