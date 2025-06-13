import uuid
from django.db import models
from django.forms import ValidationError

# Create your models here.
class HardwareItem(models.Model):
    """
    Model representing a hardware item available for loan during an event.
    Each item has a name, description, and a quantity available.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    quantity_available = models.PositiveIntegerField(default=0)
    abreviation = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(
        upload_to="hardware_images/", blank=True, null=True
    )
    event = models.ForeignKey(
        "event.Event", on_delete=models.CASCADE, blank=False, null=False
    )
    borrowers = models.ManyToManyField(
        "participant.Hacker",
        related_name="borrowed_hardware_items",
    )

    def clean(self):
        """
        Custom clean to validate each restriction of fields.
        """
        super().clean()
        errors = {}

        if self.quantity_available < 0:
            errors["quantity_available"] = "Quantity available cannot be negative."

        if errors:
            raise ValidationError(errors)
