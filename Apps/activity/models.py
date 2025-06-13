import uuid
from django.db import models
from django.core.exceptions import ValidationError
from Apps.activity.Enums.activityEnum import ActivityEnum

# Create your models here.
class Activity(models.Model):
    """
    Model representing an activity in an event.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False)

    type = models.CharField(max_length=50, choices=ActivityEnum.choices() ,blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=False, null=False)
    end_date = models.DateTimeField(blank=False, null=False)
    event = models.ForeignKey(
        "event.Event", on_delete=models.CASCADE, blank=False, null=False
    )
    hacker_participants = models.ManyToManyField(
        "participant.Hacker",
        related_name="activities",
    )
    mentor_participants = models.ManyToManyField(
        "participant.Mentor",
        related_name="activities",
    )
    sponsor_participants = models.ManyToManyField(
        "participant.Sponsor",
        related_name="activities",
    )
    volunteer_participants = models.ManyToManyField(
        "participant.Volunteer",
        related_name="activities",
    )
    admin_participants = models.ManyToManyField(
        "participant.Admin",
        related_name="activities",
    )

    def clean(self):
        """
        Custom clean to validate each restriction of fields.
        """
        super().clean()
        errors = {}

        if self.start_date > self.end_date:
            errors['start_date'] = "Start date must be before end date."
        
        if errors:
            raise ValidationError(errors)