import uuid
from django.db import models
from django.forms import ValidationError

# Create your models here.
class Warehouse(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    rows = models.IntegerField(blank=False, null=False)
    columns = models.IntegerField(blank=False, null=False)
    event = models.ForeignKey(
        "event.Event", on_delete=models.CASCADE, blank=False, null=False
    )
    luggage = models.ManyToManyField(
        "Luggage",
        related_name="warehouse",
    )

    def clean(self):
        super().clean()

        if self.rows is None or self.columns is None:
            raise ValidationError("Rows and columns cannot be None.")

        if self.rows <= 0 or self.columns <= 0:
            raise ValidationError("Rows and columns must be positive integers.")

class Luggage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(null=False)
    row_position = models.IntegerField(blank=False, null=False)
    column_position = models.IntegerField(blank=False, null=False)
    image = models.ImageField(
        upload_to="luggage_images/", blank=True, null=True
    )
    owner = models.ForeignKey(
        "participant.Hacker", on_delete=models.CASCADE, blank=False, null=False
    )

    def clean(self):
        super().clean()
        if self.row_position is None or self.column_position is None:
            raise ValidationError("Row and column positions cannot be None.")

        if self.row_position < 0 or self.column_position < 0:
            raise ValidationError("Row and column positions must be non-negative integers.")
