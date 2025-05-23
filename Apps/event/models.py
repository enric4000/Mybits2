import uuid
from django.db import models
from django.forms import ValidationError
from .Enums.timezoneEnum import TimezoneEnum

# Create your models here.
class Event(models.Model):
    """
    Model representing an event.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, unique=True, null=False)
    AppName = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    location = models.CharField(max_length=255, null=False)
    timezone = models.CharField(max_length=50, choices=TimezoneEnum.choices(), null=False)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    hacker_deadline = models.DateTimeField(null=False)
    mentor_deadline = models.DateTimeField(null=False)
    volunteer_deadline = models.DateTimeField(null=False)
    sponsor_deadline = models.DateTimeField(null=False)
    domain_link = models.URLField(max_length=200, null=True, blank=True)
    live_link = models.URLField(max_length=200, null=True, blank=True)
    x_link = models.URLField(max_length=200, null=True, blank=True)
    facebook_link = models.URLField(max_length=200, null=True, blank=True)
    instagram_link = models.URLField(max_length=200, null=True, blank=True)
    terms_and_conditions_link = models.CharField(max_length=255, null=False)
    activities_enabled = models.BooleanField(default=False)
    warehouse_enabled = models.BooleanField(default=False)
    hardware_enabled = models.BooleanField(default=False)
    judging_enabled = models.BooleanField(default=False)

    def clean(self):
        """
        Custom clean to validate each restriction of fields.
        """
        super().clean()
        errors = {}

        if self.start_date > self.end_date:
            errors['start_date'] = "Start date must be before end date."

        if self.hacker_deadline > self.end_date:
            errors['hacker_deadline'] = "Hacker deadline must be before end date."

        if self.mentor_deadline > self.end_date:
            errors['mentor_deadline'] = "Mentor deadline must be before end date."

        if self.volunteer_deadline > self.end_date:
            errors['volunteer_deadline'] = "Volunteer deadline must be before end date."

        if self.sponsor_deadline > self.end_date:
            errors['sponsor_deadline'] = "Sponsor deadline must be before end date."

        if errors:
            raise ValidationError(errors)
