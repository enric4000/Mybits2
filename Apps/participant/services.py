from itertools import chain
from .Enums.participantTypeEnum import ParticipantTypeEnum
from .forms import HackerForm, MentorForm, VolunteerForm, SponsorForm, AdminForm
from .models import Participant, Hacker, Mentor, Volunteer, Sponsor, Admin


class ParticipantService:
    """
    This class handles the operations on the participant model.
    """

    @staticmethod
    def create_participant(form):
        participant = form.save(commit=False)
        participant.save()
        return participant

    @staticmethod
    def get_event_participants(event_id):
        """
        This method returns the list of participants for a specific event.
        """

    participants = list(
        chain(
            Hacker.objects.values("id", "user", "type"),
            Mentor.objects.values("id", "user", "type"),
            Sponsor.objects.values("id", "user", "type"),
            Volunteer.objects.values("id", "user", "type"),
            Admin.objects.values("id", "user", "type"),
        )
    )

    @staticmethod
    def filter_by_name_and_email(event_id, search, participants):
        """
        This method filters the participants by name and email.
        """
        if participants is None:
            return None

        return participants.filter(
            event_id=event_id,
            participant__custom_user__name__icontains=search,
        ) | participants.filter(
            event_id=event_id, participant__custom_user__email__icontains=search
        )

    @staticmethod
    def filter_event_participants_by_type(event_id, participant_type, participants):
        """
        This method filters the participants by type.
        """
        if participants is None:
            return None

        return participants.filter(
            event_id=event_id, participant__custom_user__type=participant_type
        )

    @staticmethod
    def filter_event_participants_by_status(event_id, status, participants):
        """
        This method filters the participants by status.
        """
        if participants is None:
            return None

        return participants.filter(
            event_id=event_id, participant__custom_user__status=status
        )

    @staticmethod
    def get_participant(event_id, participant_id):
        """
        This method returns a specific participant for a specific event.
        """
        return Participant.objects.filter(event_id=event_id, id=participant_id).first()

    @staticmethod
    def is_user_admin(event_id, user):
        """
        This method checks if the user is an admin.
        """
        return not (Admin.Objects.filter(event_id=event_id, user=user).first() is None)

    @staticmethod
    def participant_form(participant):
        """
        This method returns the form for a specific participant.
        """
        if participant.type == ParticipantTypeEnum.HACKER:
            return HackerForm(instance=participant)

        elif participant.type == ParticipantTypeEnum.MENTOR:
            return MentorForm(instance=participant)

        elif participant.type == ParticipantTypeEnum.VOLUNTEER:
            return VolunteerForm(instance=participant)

        elif participant.type == ParticipantTypeEnum.SPONSOR:
            return SponsorForm(instance=participant)

        elif participant.type == ParticipantTypeEnum.ADMIN:
            return AdminForm(instance=participant)

        else:
            raise ValueError("Invalid participant type")
