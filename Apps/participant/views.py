import json
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from Apps.event.services import EventService
from .forms import AdminForm

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

        try:
            event = EventService.get_event(event_id)
            participants = ParticipantService.get_event_participants(event_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event_id, request.user):
            return HttpResponse(status=403)

        if search:
            participants = ParticipantService.filter_by_name_and_email(
                search, participants
            )

        if participant_type:
            participants = ParticipantService.filter_event_participants_by_type(
                participant_type, participants
            )

        if status:
            participants = ParticipantService.filter_event_participants_by_status(
                status, participants
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

        try:
            event = EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        participant = ParticipantService.get_participant(event_id, participant_id)

        if not participant:
            return HttpResponse(status=404)

        if request.user == participant.user:
            form = ParticipantService.get_participant_form(participant)
            return render(request, "participantEdit.html", {"form": form})

        elif ParticipantService.is_user_admin(event_id, request.user):
            participant_fields = ParticipantService.participant_to_dict(participant)
            under_review = ParticipantService.is_participant_under_review(participant)
            return render(
                request,
                "participantDetail.html",
                {
                    "fields": participant_fields,
                    "admin": True,
                    "is_under_review": under_review,
                },
                status=200,
            )
        else:
            return HttpResponse(status=403)

    def post(self, request, *args, **kwargs):
        """
        This method handles the edit of a specific participant.
        """
        participant_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")
        try:
            event = EventService.get_event(event_id)
            participant = ParticipantService.get_participant(event_id, participant_id)

        except ValueError:
            return HttpResponse(status=404)

        if not participant:
            return HttpResponse(status=404)

        if not request.user.is_authenticated or participant.user != request.user:
            return HttpResponse(status=403)

        form = ParticipantService.get_request_form(participant.type.lower(), request)

        if form.is_valid():
            participant = ParticipantService.update_participant(
                participant,
                form,
                event,
                request.user
                )
            form = ParticipantService.get_participant_form(participant)
            return render(
                request,
                "participantEdit.html",
                {"form": form, "confirmation": "Application edited successfully!"},
            )

        else:
            return render(request, "participantEdit.html", {"form": form}, status=400)

    def delete(self, request, *args, **kwargs):
        """
        This view handles the delete of a participant
        """
        participant_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")
        try:
            event = EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        participant = ParticipantService.get_participant(event_id, participant_id)

        if not participant:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False or request.user != participant.user:
            return redirect(f"/event/{event_id}/participant/{participant_id}/")

        ParticipantService.delete_participant(participant)
        return HttpResponse(status=204)


class ParticipantApplicationView(View):
    """
    This view handles the application of a participant.
    """

    def get(self, request, *args, **kwargs):
        """
        This method handles the load of a specific participant application form.
        """

        event_id = kwargs.get("event_id")
        try:
            event = EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        participant_type = request.GET.get("type")

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        participant = ParticipantService.get_participant_by_event_and_user(
            event, request.user
        )

        if participant:
            return redirect(
                "/event/"
                + str(event_id)
                + "/participant/"
                + str(participant.id)
                + "/id/"
            )

        if ParticipantService.is_email_in_admin_domain(event, request.user):
            form = AdminForm()
            return render(request, "participantApplication.html", {"form": form})

        if participant_type is None:
            opened_applications = EventService.get_opened_applications(event_id)
            return render(
                request,
                "participantType.html",
                {**opened_applications, "event_id": event_id},
            )

        else:
            form = ParticipantService.get_type_form(participant_type)

            if form is None:
                return redirect("/event/" + str(event_id) + "/participant/apply/")

            return render(request, "participantApplication.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """
        This method handles the creation of participants.
        """
        event_id = kwargs.get("event_id")
        participant_type = request.GET.get("type")
        try:
            event = EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if ParticipantService.is_email_in_admin_domain(event, request.user):
            form = ParticipantService.get_request_form("admin", request)

            if form.is_valid():
                try:
                    ParticipantService.create_participant(form, event, request.user)
                    return redirect("/event/" + str(event_id) + "/participant/")

                except ValidationError as e:
                    form.add_error(None, e)
                    return render(
                        request,
                        "participantApplication.html",
                        {"form": form},
                        status=400,
                    )

            else:
                return render(
                    request, "participantApplication.html", {"form": form}, status=400
                )

        if participant_type is None:
            return redirect("/event/" + str(event_id) + "/participant/apply/")

        form = ParticipantService.get_request_form(participant_type, request)

        if form is None:
            return HttpResponse(status=400)

        if form.is_valid():
            try:
                participant = ParticipantService.create_participant(
                    form, event, request.user
                )
                return redirect("/event/" + str(event_id) + "/participant/")

            except ValidationError as e:
                form.add_error(None, e)
                return render(
                    request,
                    "participantApplication.html",
                    {"form": form},
                    status=400,
                )

        else:
            return render(request, "participantApplication.html", {"form": form})


class ParticipantIdView(View):
    """
    This view handles the participant id. in a QR format
    """

    def get(self, request, *args, **kwargs):
        """
        This method handles the load of the a specific participant.
        """
        participant_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        participant = ParticipantService.get_participant(event_id, participant_id)

        if not participant:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False or (
            request.user != participant.user
            and not ParticipantService.is_user_admin(event_id, request.user)
        ):
            return HttpResponse(status=403)

        return render(
            request,
            "participantId.html",
            {"participant_id": participant_id},
            status=200,
        )


class ParticipantMineIdView(View):
    """
    This view handles the participant id. in a QR format
    """

    def get(self, request, *args, **kwargs):
        """
        This method handles the load of the logged user's participant Id.
        """
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return HttpResponse(status=403)

        participant = ParticipantService.get_participant_by_event_and_user(
            event, request.user
        )

        if not participant:
            return redirect("/event/" + str(event_id) + "/participant/apply/")

        return render(
            request,
            "participantId.html",
            {"participant_id": participant.id},
            status=200,
        )


class ParticipantMineView(View):
    """
    This view handles the participant of the logged user
    """

    def get(self, request, *args, **kwargs):
        """
        This method handles the load of the logged user participant.
        """
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return HttpResponse(status=403)

        participant = ParticipantService.get_participant_by_event_and_user(
            event, request.user
        )

        if not participant:
            return HttpResponse(status=400)

        return redirect(
            "/event/" + str(event_id) + "/participant/" + str(participant.id) + "/"
        )


class ParticipantCheckInView(View):
    """
    This view handles the participant id. in a QR format
    """

    def get(self, request, *args, **kwargs):
        """
        This method handles the check-in interface of participants.
        """
        event_id = kwargs.get("event_id")

        try:
            EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        if (
            request.user.is_authenticated is False
            or ParticipantService.is_user_admin(event_id, request.user) is False
        ):
            return HttpResponse(status=403)

        return render(
            request,
            "participantCheckIn.html",
            {"event_id": event_id},
            status=200,
        )

    def post(self, request, *args, **kwargs):
        """
        This method handles the check-in action of participants.
        """
        event_id = kwargs.get("event_id")

        try:
            EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        try:
            qr = json.loads(request.body).get("qrResult")

        except Exception:
            return HttpResponse(status=400)

        if (
            request.user.is_authenticated is False
            or not ParticipantService.is_user_admin(event_id, request.user)
        ):
            return HttpResponse(status=401)

        participant = ParticipantService.get_participant(event_id, qr)

        if not participant:
            return HttpResponse(status=404)

        if ParticipantService.is_participant_accepted_or_attended(participant) is False:
            return HttpResponse(status=403)

        if ParticipantService.check_in_participant(participant):
            return HttpResponse(status=200)

        else:
            return HttpResponse(status=409)


class ParticipantAcceptView(View):
    """
    This view handles a participant acceptance.
    """

    def post(self, request, *args, **kwargs):
        """
        This method handles the acceptance action of participants.
        """
        event_id = kwargs.get("event_id")
        participant_id = kwargs.get("pk")

        try:
            EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        participant = ParticipantService.get_participant(event_id, participant_id)

        if not participant:
            return HttpResponse(status=404)

        if (
            request.user.is_authenticated is False
            or not ParticipantService.is_user_admin(event_id, request.user)
        ):
            return HttpResponse(status=401)

        if ParticipantService.is_participant_under_review(participant) is False:
            return HttpResponse(status=403)

        if ParticipantService.accept_participant(participant):
            return HttpResponse(status=200)

        else:
            return HttpResponse(status=409)


class ParticipantRejectView(View):
    """
    This view handles a participant rejection.
    """

    def post(self, request, *args, **kwargs):
        """
        This method handles the rejection action of participants.
        """
        event_id = kwargs.get("event_id")
        participant_id = kwargs.get("pk")

        try:
            EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        participant = ParticipantService.get_participant(event_id, participant_id)

        if not participant:
            return HttpResponse(status=404)

        if (
            request.user.is_authenticated is False
            or not ParticipantService.is_user_admin(event_id, request.user)
        ):
            return HttpResponse(status=401)

        if ParticipantService.is_participant_under_review(participant) is False:
            return HttpResponse(status=403)

        if ParticipantService.reject_participant(participant):
            return HttpResponse(status=200)

        else:
            return HttpResponse(status=409)
