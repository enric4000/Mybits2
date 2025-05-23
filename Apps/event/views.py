from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
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
        return render(request, "events.html", {"events": events})


class EventCRUDView(View):
    def get(self, request, *args, **kwargs):
        """
        This method handles the load of an event.
        """
        # TODO: check if user is authenticated and is admin
        id = kwargs.get("pk")
        event = EventService.get_event(kwargs.get("pk"))
        if not event:
            return HttpResponse(status=404)
        form = EventForm(instance=event)
        return render(request, "eventUpdate.html", {"form": form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            event_id = kwargs.get("pk")
            if event_id:
                form = EventForm(
                    request.POST, instance=EventService.get_event(event_id)
                )
                if form.is_valid():
                    updated_event = EventService.update_event(
                        event_id, form.cleaned_data
                    )
                    return redirect("/event/" + str(updated_event.id) + "/")
                else:
                    return render(request, "eventUpdate.html", {"form": form})
            else:
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=403)

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            event_id = kwargs.get("pk")
            if event_id:
                EventService.delete_event(event_id)
                return HttpResponse(status=204)
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
        form = EventForm()
        return render(request, "eventCreation.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """
        This method handles the creation of a new event.
        """
        form = EventForm(request.POST)
        if form.is_valid():
            event = EventService.create_event(form)
            return redirect("/event/" + str(event.id) + "/")
        else:
            return render(request, "eventCreation.html", {"form": form})
