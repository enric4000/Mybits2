from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from Apps.event.services import EventService
from Apps.participant.services import ParticipantService
from Apps.warehouse.forms import LuggageForm, WarehouseForm
from Apps.warehouse.services import WarehouseService


# Create your views here.
class WarehouseView(View):
    """
    This view handles the list of warehouses
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to display the list of warehouses.
        """
        search = request.GET.get("search")
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        if search:
            warehouses = WarehouseService.search_warehouses(event, search)

        else:
            warehouses = WarehouseService.get_warehouses(event)

        return render(request, "warehouses.html", {"warehouses": warehouses})


class WarehouseCreateView(View):
    """
    This view handles the creation of a new warehouse
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to display the warehouse creation form.
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

        form = WarehouseForm()
        return render(request, "warehouseCreate.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new warehouse.
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

        form = WarehouseForm(request.POST)

        if form.is_valid():
            warehouse = WarehouseService.create_warehouse(form, event)
            return redirect(f"/event/{event_id}/warehouse/{warehouse.id}/")

        return render(request, "warehouseCreate.html", {"form": form}, status=400)


class WarehouseCRUDView(View):
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to display the warehouse details.
        """
        warehouse_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
            warehouse = WarehouseService.get_warehouse(warehouse_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        form = WarehouseForm(instance=warehouse)

        return render(request, "warehouseEdit.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to update the warehouse details.
        """
        warehouse_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
            warehouse = WarehouseService.get_warehouse(warehouse_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        form = WarehouseForm(request.POST, instance=warehouse)

        if form.is_valid():
            WarehouseService.update_warehouse(form, warehouse)
            return render(
                request,
                "warehouseEdit.html",
                {"form": form, "confirmation": "Warehouse updated successfully."},
            )

        return render(request, "warehouseEdit.html", {"form": form}, status=400)

    def delete(self, request, *args, **kwargs):
        """
        Handles DELETE requests to remove a warehouse.
        """
        warehouse_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
            warehouse = WarehouseService.get_warehouse(warehouse_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return HttpResponse(status=403)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        if WarehouseService.delete_warehouse(warehouse):
            return HttpResponse(status=204)

        return HttpResponse(status=409)


class WarehouseLuggageView(View):
    """
    This view handles the luggage in a warehouse
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to display the luggage in a warehouse.
        """
        warehouse_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
            warehouse = WarehouseService.get_warehouse(warehouse_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        luggage = WarehouseService.get_warehouse_luggage(warehouse)

        return render(request, "warehouseLuggage.html", {"luggage": luggage})


class WarehouseLuggageCreateView(View):
    """
    This view handles the creation of luggage in a warehouse
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to display the luggage creation form.
        """
        warehouse_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")
        participant_id = kwargs.get("participant_id")

        try:
            event = EventService.get_event(event_id)
            warehouse = WarehouseService.get_warehouse(warehouse_id)
            participant = ParticipantService.get_participant(event_id, participant_id)

        except ValueError:
            return HttpResponse(status=404)

        if participant is None:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        form = LuggageForm()

        return render(request, "luggageCreate.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create new luggage in a warehouse.
        """
        warehouse_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")
        participant_id = kwargs.get("participant_id")

        try:
            event = EventService.get_event(event_id)
            warehouse = WarehouseService.get_warehouse(warehouse_id)
            participant = ParticipantService.get_participant(event_id, participant_id)

        except ValueError:
            return HttpResponse(status=404)

        if participant is None:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        form = LuggageForm(request.POST, request.FILES)

        if form.is_valid():
            luggage = WarehouseService.create_luggage(form, warehouse, participant)
            if luggage is None:
                return render(
                    request,
                    "luggageCreate.html",
                    {"form": form, "postionError": "That position is already occupied or is out of limits."},status=400
                )
            return redirect(
                f"/event/{event_id}/warehouse/{warehouse_id}/participant/{participant.id}/"
            )

        return render(request, "luggageCreate.html", {"form": form}, status=400)


class WarehouseLuggageCRUDView(View):
    """
    This view handles the CRUD operations for luggage in a warehouse
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to display the luggage details.
        """
        warehouse_id = kwargs.get("pk")
        luggage_id = kwargs.get("luggage_id")
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
            WarehouseService.get_warehouse(warehouse_id)
            luggage = WarehouseService.get_luggage(luggage_id)

        except Exception:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        form = LuggageForm(instance=luggage)

        return render(request, "luggageEdit.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to update the luggage details.
        """
        warehouse_id = kwargs.get("pk")
        luggage_id = kwargs.get("luggage_id")
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
            warehouse = WarehouseService.get_warehouse(warehouse_id)
            luggage = WarehouseService.get_luggage(luggage_id)

        except Exception:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        form = LuggageForm(request.POST, request.FILES, instance=luggage)

        if form.is_valid():
            luggage = WarehouseService.update_luggage(form, luggage, warehouse)
            if luggage is None:
                form.add_error(None, "That position is already occupied or is out of limits.")
                return render(
                    request,
                    "luggageEdit.html",
                    {"form": form, "postionError": "That position is already occupied or is out of limits."},
                    status=400,
                )

            form = LuggageForm(instance=luggage)
            return render(
                request,
                "luggageEdit.html",
                {"form": form, "confirmation": "Luggage updated successfully."},
            )

        return render(request, "luggageEdit.html", {"form": form}, status=400)

    def delete(self, request, *args, **kwargs):
        """
        Handles DELETE requests to remove a piece of luggage.
        """
        warehouse_id = kwargs.get("pk")
        luggage_id = kwargs.get("luggage_id")
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
            warehouse = WarehouseService.get_warehouse(warehouse_id)
            luggage = WarehouseService.get_luggage(luggage_id)

        except Exception:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return HttpResponse(status=403)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        if WarehouseService.delete_luggage(luggage, warehouse):
            return HttpResponse(status=204)

        return HttpResponse(status=409)

class WarehouseLuggageByParticipantView(View):
    """
    This view handles the luggage by participant in a warehouse
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to display the luggage in a warehouse.
        """
        warehouse_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")
        participant_id = kwargs.get("participant_id")

        try:
            event = EventService.get_event(event_id)
            warehouse = WarehouseService.get_warehouse(warehouse_id)

        except ValueError:
            return HttpResponse(status=404)


        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        participant = ParticipantService.get_participant(event_id, participant_id)

        if participant is None:
            return render(request, "warehouseParticipant.html", status=400)

        luggage = WarehouseService.get_warehouse_luggage_by_participant(warehouse, participant)

        return render(request, "warehouseLuggage.html", {"luggage": luggage, "event_id": event_id, "warehouse_id": warehouse_id, "participant_id": participant_id})
