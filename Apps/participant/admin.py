from django.contrib import admin

from Apps.participant.models import Hacker, Volunteer, Mentor, Sponsor, Admin


# Register your models here.
@admin.register(Hacker)
class HackerAdmin(admin.ModelAdmin):
    list_display = ("id", "get_user_first_name", "get_user_email", "application_date")
    search_fields = ("user__first_name", "user__email")
    list_filter = ("application_date",)
    ordering = ("-application_date",)

    @admin.display(description="First Name")
    def get_user_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description="Email")
    def get_user_email(self, obj):
        return obj.user.email


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("id", "get_user_first_name", "get_user_email", "application_date")
    search_fields = ("user__first_name", "user__email")
    list_filter = ("application_date",)
    ordering = ("-application_date",)

    @admin.display(description="First Name")
    def get_user_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description="Email")
    def get_user_email(self, obj):
        return obj.user.email


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ("id", "get_user_first_name", "get_user_email", "application_date")
    search_fields = ("user__first_name", "user__email")
    list_filter = ("application_date",)
    ordering = ("-application_date",)

    @admin.display(description="First Name")
    def get_user_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description="Email")
    def get_user_email(self, obj):
        return obj.user.email


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ("id", "get_user_first_name", "get_user_email", "application_date")
    search_fields = ("user__first_name", "user__email")
    list_filter = ("application_date",)
    ordering = ("-application_date",)

    @admin.display(description="First Name")
    def get_user_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description="Email")
    def get_user_email(self, obj):
        return obj.user.email


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ("id", "get_user_first_name", "get_user_email", "application_date")
    search_fields = ("user__first_name", "user__email")
    list_filter = ("application_date",)
    ordering = ("-application_date",)

    @admin.display(description="First Name")
    def get_user_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description="Email")
    def get_user_email(self, obj):
        return obj.user.email
