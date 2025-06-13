import uuid
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Team(models.Model):
    """
    Model representing a team of participants in an event.
    A team can have up to 4 members and is associated with a specific event.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    members = models.ManyToManyField(
        "participant.Hacker",
        related_name="teams",
    )
    event = models.ForeignKey(
        "event.Event", on_delete=models.CASCADE, blank=False, null=False
    )

    def clean(self):
        super().clean()
        if self.members.all().count() > 4:
            raise ValidationError("A team cannot have more than 4 participants.")
