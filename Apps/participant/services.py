from itertools import chain
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.utils.timezone import now
from .Enums.participantTypeEnum import ParticipantTypeEnum
from .forms import HackerForm, MentorForm, VolunteerForm, SponsorForm, AdminForm
from .models import Hacker, Mentor, Volunteer, Sponsor, Admin


class ParticipantService:
    """
    This class handles the operations on the participant model.
    """

    @staticmethod
    def create_participant(form, event, user):
        if (
            Hacker.objects.filter(event=event, user=user).first()
            or Mentor.objects.filter(event=event, user=user).first()
            or Volunteer.objects.filter(event=event, user=user).first()
            or Sponsor.objects.filter(event=event, user=user).first()
            or Admin.objects.filter(event=event, user=user).first()
        ):
            raise ValidationError("You have already applied to this event!")
        participant = form.save(commit=False)
        participant.event = event
        participant.user = user
        participant.type = form.type.value
        participant.save()
        return participant

    @staticmethod
    def update_participant(participant, form, event, user):
        """
        This method updates a participant.
        """
        for key, value in form.cleaned_data.items():
            setattr(participant, key, value)
        participant.event = event
        participant.user = user
        participant.type = form.type.value
        participant.save()
        return participant

    @staticmethod
    def delete_participant(participant):
        participant.delete()

    @staticmethod
    def get_event_participants(event_id):
        """
        This method returns the list of participants for a specific event.
        """

        participants = Hacker.objects.filter(event_id=event_id).first()
        participants = list(
            chain(
                Hacker.objects.select_related("user")
                .filter(event_id=event_id)
                .values(
                    "id",
                    "user__id",
                    "user__username",
                    "user__first_name",
                    "user__last_name",
                    "user__email",
                    "user__pronoun",
                    "type",
                    "status",
                ),
                Mentor.objects.select_related("user")
                .filter(event_id=event_id)
                .values(
                    "id",
                    "user__id",
                    "user__username",
                    "user__first_name",
                    "user__last_name",
                    "user__email",
                    "user__pronoun",
                    "type",
                    "status",
                ),
                Sponsor.objects.select_related("user")
                .filter(event_id=event_id)
                .values(
                    "id",
                    "user__id",
                    "user__username",
                    "user__first_name",
                    "user__last_name",
                    "user__email",
                    "user__pronoun",
                    "type",
                    "status",
                ),
                Volunteer.objects.select_related("user")
                .filter(event_id=event_id)
                .values(
                    "id",
                    "user__id",
                    "user__username",
                    "user__first_name",
                    "user__last_name",
                    "user__email",
                    "user__pronoun",
                    "type",
                    "status",
                ),
                Admin.objects.select_related("user")
                .filter(event_id=event_id)
                .values(
                    "id",
                    "user__id",
                    "user__username",
                    "user__first_name",
                    "user__last_name",
                    "user__email",
                    "user__pronoun",
                    "type",
                    "status",
                ),
            )
        )
        return participants

    @staticmethod
    def filter_by_name_and_email(search, participants):
        """
        This method filters the participants by name and email.
        """
        if participants is None:
            return None

        return [
            p
            for p in participants
            if (search.lower()
            in (
                p.get("user__first_name", "").lower()
                + " "
                + p.get("user__last_name", "").lower()
            )
            or search.lower() in p.get("user__email", "").lower()
            or search.lower() in p.get("user__username", "").lower())
        ]

    @staticmethod
    def filter_event_participants_by_type(participant_type, participants):
        """
        This method filters the participants by type.
        """
        if participants is None:
            return None

        return [
            p
            for p in participants
            if p.get("type", "").lower() == participant_type.lower()
        ]

    @staticmethod
    def filter_event_participants_by_status(status, participants):
        """
        This method filters the participants by status.
        """
        if participants is None:
            return None

        return [
            p
            for p in participants
            if p.get("status", "").lower().replace("_", " ")
            == status.lower().replace("_", " ")
        ]

    @staticmethod
    def get_participant(event_id, participant_id):
        """
        This method returns a specific participant for a specific event.
        """
        participant = (
            Hacker.objects.filter(event_id=event_id, id=participant_id).first()
            or Mentor.objects.filter(event_id=event_id, id=participant_id).first()
            or Volunteer.objects.filter(event_id=event_id, id=participant_id).first()
            or Sponsor.objects.filter(event_id=event_id, id=participant_id).first()
            or Admin.objects.filter(event_id=event_id, id=participant_id).first()
        )
        return participant

    @staticmethod
    def get_participant_by_event_and_user(event, user):
        """
        This method returns a specific participant for a specific event.
        """
        participant = (
            Hacker.objects.filter(event=event, user=user).first()
            or Mentor.objects.filter(event=event, user=user).first()
            or Volunteer.objects.filter(event=event, user=user).first()
            or Sponsor.objects.filter(event=event, user=user).first()
            or Admin.objects.filter(event=event, user=user).first()
        )
        return participant

    @staticmethod
    def get_participant_form(participant):
        """
        This method return the specific form for a participant
        """
        form = None
        type = participant.type.lower()

        if type == "hacker":
            form = HackerForm(instance=participant)

        elif type == "mentor":
            form = MentorForm(instance=participant)

        elif type == "volunteer":
            form = VolunteerForm(instance=participant)

        elif type == "sponsor":
            form = SponsorForm(instance=participant)

        elif type == "admin":
            form = AdminForm(instance=participant)

        return form

    @staticmethod
    def get_request_form(participant_type, request):
        """
        This method return the specific form from a request
        """
        form = None

        if participant_type == "hacker":
            form = HackerForm(request.POST)
            form.type = ParticipantTypeEnum.HACKER

        elif participant_type == "mentor":
            form = MentorForm(request.POST)

        elif participant_type == "volunteer":
            form = VolunteerForm(request.POST)
            form.type = ParticipantTypeEnum.VOLUNTEER

        elif participant_type == "sponsor":
            form = SponsorForm(request.POST)
            form.type = ParticipantTypeEnum.SPONSOR

        elif participant_type == "admin":
            form = AdminForm(request.POST)
            form.type = ParticipantTypeEnum.ADMIN

        return form

    @staticmethod
    def get_type_form(participant_type):
        """
        This method return the specific form from a type
        """
        form = None

        if participant_type == "hacker":
            form = HackerForm()

        elif participant_type == "mentor":
            form = MentorForm()

        elif participant_type == "volunteer":
            form = VolunteerForm()

        elif participant_type == "sponsor":
            form = SponsorForm()

        return form

    @staticmethod
    def is_user_admin(event, user):
        """
        This method checks if the user is an admin.
        """
        return Admin.objects.filter(event=event, user=user).first() is not None

    @staticmethod
    def get_participant_admin(event, user):
        """
        This method returns a specific participant for a specific event.
        """
        participant = Admin.objects.filter(event=event, user=user).first()
        return participant

    @staticmethod
    def is_email_in_admin_domain(event, user):
        """
        This method checks if the user is an admin.
        """
        user_domain = user.email.split("@")[-1]
        event_domain = (
            event.domain_link.replace("https://", "")
            .replace("http://", "")
            .replace("www.", "")
        )
        return user_domain == event_domain

    @staticmethod
    def participant_to_dict(participant):
        participant_dict = model_to_dict(participant)
        return [
            {"name": key, "value": value} for key, value in participant_dict.items()
        ]

    @staticmethod
    def create_default_admin(event, user):
        """
        This method creates a default admin for the event.
        """
        admin = Admin(
            event=event,
            user=user,
            accepted_date=None,
            phone_number="+00000000000",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="L",
            origin="Unknown",
        )
        admin.save()
        return admin

    @staticmethod
    def is_participant_accepted_or_attended(participant):
        """
        This method checks if the participant is accepted.
        """
        return (
            participant.status.lower() == "confirmed"
            or participant.status.lower() == "attended"
        )

    @staticmethod
    def check_in_participant(participant):
        """
        This method checks in a participant.
        """
        if participant.status.lower() == "attended":
            return False

        participant.status = "ATTENDED"
        participant.save()
        return True

    @staticmethod
    def is_participant_under_review(participant):
        """
        This method returns true if the participant is under review.
        """
        return participant.status.lower().replace("_", " ") == "under review"

    @staticmethod
    def accept_participant(participant):
        """
        This method accepts a participant.
        """
        if participant.status.lower().replace("_", " ") == "under review":
            participant.accepted_date = now()
            participant.status = "CONFIRMED"
            participant.save()
            return True
        return False

    @staticmethod
    def reject_participant(participant):
        """
        This method rejects a participant.
        """
        if participant.status.lower().replace("_", " ") == "under review":
            participant.status = "REJECTED"
            participant.save()
            return True
        return False

    @staticmethod
    def get_participant_diet(participant):
        """
        This method returns the diet of a participant.
        """
        if participant.user.dietary_other:
            return participant.user.dietary_other

        return participant.user.dietary
