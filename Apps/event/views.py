from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.utils.timezone import now

from Apps.participant.services import ParticipantService
from .forms import EventForm
from .services import EventService

# TODO: check if user is authenticated and is admin/ view to see your own events / check delete


class EventView(View):
    """
    This view handles the render of the list of users with or without filters.
    """

    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        search = request.GET.get("search")
        if search:
            events = EventService.find_by_name_and_appName(search)
        else:
            events = EventService.get_first_100_events()
        return render(request, "events.html", {"events": events, "today": now()})


class EventCRUDView(View):
    def get(self, request, *args, **kwargs):
        """
        This method handles the load of an event.
        """
        # TODO: check if user is authenticated and is admin
        id = kwargs.get("pk")
        if not request.user.is_authenticated:
            return HttpResponse(status=403)

        try:
            event = EventService.get_event(kwargs.get("pk"))
        except ValueError:
            return HttpResponse(status=404)

        if ParticipantService.is_user_admin(event, request.user):
            form = EventForm(instance=event)
            return render(request, "eventUpdate.html", {"form": form})
        else:
            is_participant = (
                ParticipantService.get_participant_by_event_and_user(
                    event, request.user
                )
                is not None
            )
            event_fields = EventService.event_to_dict(event)
            return render(
                request,
                "eventDetail.html",
                {"fields": event_fields, "is_participant": is_participant},
            )

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            event_id = kwargs.get("pk")
            if event_id:
                try:
                    event = EventService.get_event(event_id)
                    form = EventForm(request.POST, instance=event)

                except ValueError:
                    return HttpResponse(status=404)

                if form.is_valid():
                    if ParticipantService.is_user_admin(event, request.user):
                        form.instance.id = event_id
                        updated_event = EventService.update_event(
                            event_id, form.cleaned_data
                        )
                        form = EventForm(instance=updated_event)
                        return render(
                            request,
                            "eventUpdate.html",
                            {
                                "form": form,
                                "confirmation": "Event updated successfully!",
                            },
                        )
                    else:
                        return HttpResponse(status=403)

                else:
                    return render(
                        request, "eventUpdate.html", {"form": form}, status=400
                    )

            else:
                return HttpResponse(status=400)

        else:
            return HttpResponse(status=403)

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            event_id = kwargs.get("pk")

            if event_id:
                try:
                    EventService.get_event(event_id)

                    if not ParticipantService.is_user_admin(
                        EventService.get_event(event_id), request.user
                    ):
                        return HttpResponse(status=403)

                    EventService.delete_event(event_id)
                    return HttpResponse(status=204)

                except ValueError:
                    return HttpResponse(status=404)

            else:
                return HttpResponse(status=400)

        else:
            return redirect("/event")


class EventCreationView(View):
    """
    This view handles the render of the event form.
    """

    def get(self, request, *args, **kwargs):
        """
        This method handles the creation of a new event.
        """
        if not request.user.is_authenticated:
            return HttpResponse(status=403)

        form = EventForm()
        return render(request, "eventCreation.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """
        This method handles the creation of a new event.
        """
        if not request.POST:
            return HttpResponse(status=400)

        form = EventForm(request.POST)

        if not request.user.is_authenticated:
            form.add_error(None, "User must be authenticated to create an event.")
            return render(request, "eventCreation.html", {"form": form}, status=403)

        if form.is_valid():
            event = EventService.create_event(form)
            admin = ParticipantService.create_default_admin(event, request.user)
            return redirect(
                "/event/" + str(event.id) + "/participant/" + str(admin.id) + "/"
            )

        else:
            return render(request, "eventCreation.html", {"form": form}, status=400)
