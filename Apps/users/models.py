import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from Apps.users.Enums.dietaryEnum import DietaryEnum
from Apps.users.Enums.genderEnum import GenderEnum
from datetime import date


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        extra_fields["date_of_birth"] = date.today()
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    email = models.EmailField(unique=True, null=False)
    emailVerified = models.BooleanField(default=False)
    password = models.CharField(max_length=150, null=False, blank=False)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    gender = models.CharField(max_length=20, choices=GenderEnum.choices(), blank=False)
    gender_other = models.CharField(max_length=10, blank=True)
    pronoun = models.CharField(max_length=10, blank=False)
    date_of_birth = models.DateField(blank=False, null=False)
    dietary = models.CharField(
        max_length=20, choices=DietaryEnum.choices(), blank=False
    )
    dietary_other = models.CharField(max_length=20, blank=True)
    origin = models.CharField(max_length=20, blank=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        []
    )  # This is just for the superuser creation, the rest of the fields are required in the form and by the not null check in the model!

    def clean(self):
        """
        Custom clean to validate each restriction of fields.
        """
        super().clean()
        errors = {}
        if (self.dietary == "Other") and not self.dietary_other:
            errors["dietary"] = "Please specify your dietary preference."

        if (self.dietary != "Other") and self.dietary_other:
            errors["dietary"] = (
                "Dietary preference should be 'Other' to specify a custom value."
            )

        if (self.gender == "Other") and not self.gender_other:
            errors["gender"] = "Please specify your gender or select Not specified."

        if (self.gender != "Other") and self.gender_other:
            errors["gender"] = "Gender should be 'Other' to specify a custom value."

        if errors:
            raise ValidationError(errors)
