import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from Apps.event.services import EventService
from Apps.hardware.forms import HardwareItemForm
from Apps.hardware.services import HardwareItemService
from Apps.participant.services import ParticipantService


# Create your views here.
class HardwareItemView(View):
    """
    This view handles the display of hardware items available for loan during an event.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to display hardware items.
        """
        search = request.GET.get("search")
        event_id = kwargs.get("event_id")
        try:
            event = EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        participant = ParticipantService.get_participant_by_event_and_user(
            event, request.user
        )

        if participant is None:
            return redirect("/event/" + event_id + "/participant/apply/")

        if search:
            hardware_items = HardwareItemService.search_hardware_items(event, search)

        else:
            hardware_items = HardwareItemService.get_hardware_items(event)

        if ParticipantService.is_user_admin(event, request.user):
            return render(
                request, "hardwareItems.html", {"hardware_items": hardware_items}
            )

        hardware_items = HardwareItemService.available_hardware_items(hardware_items)
        return render(request, "hardwareItems.html", {"hardware_items": hardware_items})


class HardwareItemCreateView(View):
    """
    This view handles the creation of new hardware items.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to display the hardware item creation form.
        """
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        form = HardwareItemForm()
        return render(request, "hardwareItemCreate.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new hardware item.
        """
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        form = HardwareItemForm(request.POST, request.FILES)

        if form.is_valid():
            hardware_item = HardwareItemService.create_hardware_item(form, event)
            return redirect(f"/event/{event_id}/hardware/{hardware_item.id}/")

        return render(request, "hardwareItemCreate.html", {"form": form}, status=400)


class HardwareItemCRUDView(View):
    """
    This view handles the CRUD operations for hardware items.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to display a specific hardware item.
        """
        event_id = kwargs.get("event_id")
        hardware_item_id = kwargs.get("pk")

        try:
            event = EventService.get_event(event_id)
            hardware_item = HardwareItemService.get_hardware_item(hardware_item_id)

        except ValueError:
            return HttpResponse(status=404)
    
        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            fields = HardwareItemService.hardware_item_to_dict(hardware_item)
            return render(request, "hardwareItemDetail.html", {"fields": fields})

        form = HardwareItemForm(instance=hardware_item)
        return render(
            request,
            "hardwareItemEdit.html",
            {"form": form, "hardware_item": hardware_item},
        )

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to update a specific hardware item.
        """
        event_id = kwargs.get("event_id")
        hardware_item_id = kwargs.get("pk")

        try:
            event = EventService.get_event(event_id)
            hardware_item = HardwareItemService.get_hardware_item(hardware_item_id)
        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        form = HardwareItemForm(request.POST, request.FILES)

        if form.is_valid():
            updated_hardware_item = HardwareItemService.update_hardware_item(
                form, hardware_item
            )
            form = HardwareItemForm(instance=updated_hardware_item)
            return render(
                request,
                "hardwareItemEdit.html",
                {"form": form, "confirmation": "Hardware item updated succesfully"},
                status=200,
            )

        return render(
            request,
            "hardwareItemEdit.html",
            {"form": form, "hardware_item": hardware_item},
            status=400,
        )

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests to delete a specific hardware item.
        """
        event_id = kwargs.get("event_id")
        hardware_item_id = kwargs.get("pk")

        try:
            event = EventService.get_event(event_id)
            hardware_item = HardwareItemService.get_hardware_item(hardware_item_id)
        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        HardwareItemService.delete_hardware_item(hardware_item)
        return HttpResponse(status=204)


class HardwareItemBorrowView(View):
    """
    This view handles the borrowing of hardware items by participants.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to borrow a hardware item.
        """
        event_id = kwargs.get("event_id")
        hardware_item_id = kwargs.get("pk")

        try:
            event = EventService.get_event(event_id)
            HardwareItemService.get_hardware_item(hardware_item_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        return render(request, "hardwareItemBorrow.html")

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to borrow a hardware item.
        """
        event_id = kwargs.get("event_id")
        hardware_item_id = kwargs.get("pk")

        try:
            event = EventService.get_event(event_id)
            hardware_item = HardwareItemService.get_hardware_item(hardware_item_id)
            qr = json.loads(request.body).get("qrResult")

        except ValueError:
            return HttpResponse(status=404)

        participant = ParticipantService.get_participant(event_id, qr)

        if participant is None:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        if HardwareItemService.borrow_hardware_item(hardware_item, participant):
            return HttpResponse(status=200)

        else:
            return HttpResponse(status=409)


class HardwareItemReturnView(View):
    """
    This view handles the return of borrowed hardware items by participants.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to borrow a hardware item.
        """
        event_id = kwargs.get("event_id")
        hardware_item_id = kwargs.get("pk")

        try:
            event = EventService.get_event(event_id)
            HardwareItemService.get_hardware_item(hardware_item_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        return render(request, "hardwareItemReturn.html")

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to return a borrowed hardware item.
        """
        event_id = kwargs.get("event_id")
        hardware_item_id = kwargs.get("pk")

        try:
            event = EventService.get_event(event_id)
            hardware_item = HardwareItemService.get_hardware_item(hardware_item_id)
            qr = json.loads(request.body).get("qrResult")

        except ValueError:
            return HttpResponse(status=404)

        participant = ParticipantService.get_participant(event_id, qr)

        if participant is None:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        if HardwareItemService.return_hardware_item(hardware_item, participant):
            return HttpResponse(status=200)

        else:
            return HttpResponse(status=400)
