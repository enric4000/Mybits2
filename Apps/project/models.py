import uuid
from django.db import models
from django.forms import ValidationError

# Create your models here.
class Project(models.Model):
    """
    Model representing a project of a specific team in a hackathon.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=False)
    description = models.TextField(blank=False, null=False)
    github_link = models.URLField(blank=False, null=False)
    devpost_link = models.URLField(blank=False, null=False)
    team = models.ForeignKey(
        'team.Team',
        on_delete=models.CASCADE,
        related_name='projects',
        null=False
    )

class Valoration(models.Model):
    """
    Model representing a valoration given by an admin to a project.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    score = models.IntegerField(null=False, blank=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='valuations',
        null=False
    )
    admin = models.ForeignKey(
        'participant.Admin',
        on_delete=models.CASCADE,
        related_name='valorations',
        null=False
    )


    def clean(self):
        super().clean()
        if not self.score:
            raise ValidationError("Score cannot be null or empty.")

        if self.score < 1 or self.score > 10:
            raise ValidationError("Score must be between 1 and 10.")