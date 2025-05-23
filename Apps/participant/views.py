from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from Apps.event.services import EventService
from Apps.participant.Enums.participantTypeEnum import ParticipantTypeEnum
from .forms import SponsorForm, MentorForm, VolunteerForm, HackerForm, AdminForm

from .services import ParticipantService


# Create your views here.
class ParticipantView(View):
    """
    This view handles the render of the list of participant with or without filters.
    """

    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        event_id = kwargs.get("event_id")
        search = request.GET.get("search")
        participant_type = request.GET.get("type")
        status = request.GET.get("status")

        participants = ParticipantService.get_event_participants(event_id)

        if search:
            participants = ParticipantService.filter_by_name_and_email(
                event_id, search, participants
            )

        if participant_type:
            participants = ParticipantService.filter_event_participants_by_type(
                event_id, participant_type, participants
            )

        if status:
            participants = ParticipantService.filter_event_participants_by_status(
                event_id, status, participants
            )

        return render(request, "participants.html", {"participants": participants})


class ParticipantCRUDView(View):
    """
    This view handles the CRUD of a participant.
    """

    def get(self, request, *args, **kwargs):
        """
        This method handles load of a specific participant, or the creation of a new participant.
        """
        participant_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")

        if participant_id:
            participant = ParticipantService.get_participant(event_id, participant_id)

            if not participant:
                return HttpResponse(status=404)

            form = ParticipantService.get_participant_form(participant)
            return render(request, "participantDetail.html", {"form": form})

        else:
            return HttpResponse(status=400)


class ParticipantApplicationView(View):
    """
    This view handles the application of a participant.
    """

    def get(self, request, *args, **kwargs):
        """
        This method handles the load of a specific participant application form.
        """

        event_id = kwargs.get("event_id")
        participant_type = request.GET.get("type")

        if request.user.is_authenticated is False:
            return redirect("/user/login?next=" + request.path)

        if participant_type is None:
            opened_applications = EventService.get_opened_applications(event_id)
            return render(
                request,
                "participantType.html",
                {**opened_applications, "event_id": event_id},
            )

        else:
            form = None

            if participant_type == "hacker":
                form = HackerForm()

            elif participant_type == "mentor":
                form = MentorForm()

            elif participant_type == "volunteer":
                form = VolunteerForm()

            elif participant_type == "sponsor":
                form = SponsorForm()

            else:
                return redirect("/event/" + str(event_id) + "/participant/apply/")

            return render(request, "participantApplication.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """
        This method handles the creation of participants.
        """
        event_id = kwargs.get("event_id")
        participant_type = request.GET.get("type")

        if request.user.is_authenticated is False:
            return redirect("/user/login?next=" + request.path)

        if participant_type is None:
            return redirect("/event/" + str(event_id) + "/participant/apply/")

        if participant_type == "hacker":
            form = HackerForm(request.POST)
            form.type = ParticipantTypeEnum.HACKER
            form.fields["type"].initial = ParticipantTypeEnum.HACKER

        elif participant_type == "mentor":
            form = MentorForm(request.POST)
            form.type = ParticipantTypeEnum.MENTOR

        elif participant_type == "volunteer":
            form = VolunteerForm(request.POST)
            form.type = ParticipantTypeEnum.VOLUNTEER

        elif participant_type == "sponsor":
            form = SponsorForm(request.POST)
            form.type = ParticipantTypeEnum.SPONSOR

        elif participant_type == "admin":
            form = AdminForm(request.POST)
            form.type = ParticipantTypeEnum.ADMIN

        else:
            return HttpResponse(status=400)

        form.user = request.user
        form.event = EventService.get_event(event_id)

        if form.is_valid():
            ParticipantService.create_participant(form)
            return redirect("/event/" + str(event_id) + "/participant/apply/")

        else:
            return render(request, "participantApplication.html", {"form": form})
