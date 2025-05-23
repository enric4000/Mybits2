import uuid
from django.db import models
from django.forms import ValidationError
from .Enums.participantTypeEnum import ParticipantTypeEnum
from .Enums.statusEnum import StatusEnum
from .Enums.tShirtSizeEnum import TShirtSizeEnum
from .Enums.englishLevelEnum import EnglishLevelEnum


# Create your models here.
class Participant(models.Model):
    """
    Abstract model representing a participant in the event.
    This model is inherited by other participant types such as Hacker, Mentor, etc.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    accepted_date = models.DateTimeField(blank=True, null=True)
    application_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    type = models.CharField(
        choices=ParticipantTypeEnum.choices(), blank=False, null=False
    )
    accepted_terms_and_conditions = models.BooleanField(
        default=False, blank=False, null=False
    )
    t_shirt_size = models.CharField(
        choices=TShirtSizeEnum.choices(), blank=False, null=False
    )
    origin = models.CharField(max_length=255, blank=False, null=False)
    status = models.CharField(
        default=StatusEnum.UNDER_REVIEW,
        choices=StatusEnum.choices(),
        blank=False,
        null=False,
    )
    event = models.ForeignKey(
        "event.Event", on_delete=models.CASCADE, blank=False, null=False
    )
    user = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, blank=False, null=False
    )

    def clean(self):
        """
        Custom clean to validate each restriction of fields.
        """
        super().clean()
        errors = {}

        if self.accepted_terms_and_conditions is False:
            errors["accepted_terms_and_conditions"] = (
                "You must accept the terms and conditions."
            )

        if (
            str(self.phone_number).startswith("+")
            and not str(self.phone_number)[1:].isdigit()
        ):
            errors["phone_number"] = (
                "Phone number must start with a '+' followed by digits."
            )

        if len(self.phone_number) > 17:
            errors["phone_number"] = (
                "Phone number must be less than 17 characters long."
            )

        if errors:
            raise ValidationError(errors)

    class Meta:
        abstract = True


class Hacker(Participant):
    """
    Model representing a hacker.
    """

    university = models.CharField(max_length=255, blank=False, null=False)
    degree = models.CharField(max_length=255, blank=False, null=False)
    graduation_year = models.IntegerField(blank=False, null=False)
    under_age = models.BooleanField(blank=False, null=False)
    lenny_face = models.CharField(max_length=255, blank=False, null=False)
    hear_about_us = models.CharField(max_length=255, blank=False, null=False)
    why_excited = models.TextField(blank=False, null=False)
    first_hackathon = models.BooleanField(blank=False, null=False)
    personal_projects = models.TextField(blank=False, null=False)
    github = models.URLField(max_length=200, blank=True, null=True)
    devpost = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    personal = models.URLField(max_length=200, blank=True, null=True)
    cv = models.FileField(upload_to="cv/hacker/", blank=True, null=True)
    share_cv = models.BooleanField(blank=False, null=False)
    subscribe = models.BooleanField(blank=False, null=False)

    def clean(self):
        """
        Custom clean to validate each restriction of fields.
        """
        super().clean()

        if self.type != ParticipantTypeEnum.HACKER:
            raise ValidationError(
                "Participant type must be Hacker to fill this application."
            )

        errors = {}

        if self.graduation_year < 2023:
            errors["graduation_year"] = "Graduation year must be 2023 or later."

        if errors:
            raise ValidationError(errors)


class Mentor(Participant):
    """
    Model representing a mentor.
    """

    university = models.CharField(max_length=255, blank=True, null=True)
    degree = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    english_level = models.IntegerField(
        choices=EnglishLevelEnum.choices(), blank=False, null=False
    )
    hear_about_us = models.CharField(max_length=255, blank=False, null=False)
    personal_projects = models.TextField(blank=False, null=False)
    github = models.URLField(max_length=200, blank=True, null=True)
    devpost = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    personal = models.URLField(max_length=200, blank=True, null=True)
    first_hackathon = models.BooleanField(blank=False, null=False)
    cv = models.FileField(upload_to="cv/mentor/", blank=True, null=True)
    subscribe = models.BooleanField(blank=False, null=False)

    def clean(self):
        """
        Custom clean to validate each restriction of fields.
        """
        super().clean()

        if self.type != ParticipantTypeEnum.MENTOR:
            raise ValidationError(
                "Participant type must be Mentor to fill this application."
            )

        errors = {}

        if self.degree is None and self.university is None:
            errors["degree"] = "You must provide either a degree or a university."
            errors["university"] = "You must provide either a degree or a university."

        if errors:
            raise ValidationError(errors)


class Sponsor(Participant):
    """
    Model representing a sponsor.
    """

    company_name = models.CharField(max_length=255, blank=False, null=False)
    position = models.CharField(max_length=255, blank=False, null=False)

    def clean(self):
        """
        Custom clean to validate each restriction of fields.
        """
        super().clean()

        if self.type != ParticipantTypeEnum.SPONSOR:
            raise ValidationError(
                "Participant type must be Sponsor to fill this application."
            )


class Volunteer(Participant):
    """
    Model representing a volunteer.
    """

    university = models.CharField(max_length=255, blank=True, null=True)
    degree = models.CharField(max_length=255, blank=False, null=False)
    position = models.CharField(max_length=255, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=False, null=False)
    first_volunteering = models.BooleanField(blank=False, null=False)
    hear_about_us = models.CharField(max_length=255, blank=False, null=False)
    cool_skill = models.CharField(blank=False, null=False)
    personal_qualities = models.CharField(blank=False, null=False)
    personal_weakness = models.CharField(blank=False, null=False)
    motivation = models.TextField(blank=False, null=False)
    nigth_shifts = models.BooleanField(blank=False, null=False)
    subscribe = models.BooleanField(blank=False, null=False)

    def clean(self):
        """
        Custom clean to validate each restriction of fields.
        """
        super().clean()

        if self.participant_type != ParticipantTypeEnum.VOLUNTEER:
            raise ValidationError(
                "Participant type must be Volunteer to fill this application."
            )


class Admin(Participant):
    """
    Model representing an admin.
    """

    def clean(self):
        """
        Custom clean to validate each restriction of fields.
        """
        super().clean()

        if self.type != ParticipantTypeEnum.ADMIN:
            raise ValidationError(
                "Participant type must be Admin to fill this application."
            )
