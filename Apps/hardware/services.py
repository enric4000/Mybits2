
from django.forms import model_to_dict
from Apps.hardware.models import HardwareItem
from django.db.models import Q

class HardwareItemService:
    @staticmethod
    def search_hardware_items(event, search):
        """
        Search for hardware items based on a search term.
        :param event: The event to search within.
        :param search: The search term.
        :return: A list of hardware items matching the search term.
        """
        return HardwareItem.objects.filter(
            event=event
        ).filter(
            Q(name__icontains=search) | Q(abreviation__icontains=search)
        )

    @staticmethod
    def get_hardware_items(event):
        """
        Retrieve all hardware items for a given event.
        :param event: The event to retrieve hardware items for.
        :return: A queryset of hardware items.
        """
        return HardwareItem.objects.filter(event=event)

    @staticmethod
    def available_hardware_items(hardware_items):
        """
        Filter hardware items to only include those that are available for loan.
        :param hardware_items: A queryset of hardware items.
        :return: A queryset of available hardware items.
        """
        return hardware_items.filter(quantity_available__gt=0)

    @staticmethod
    def create_hardware_item(form, event):
        """
        Create a new hardware item.
        :param form: The form containing the hardware item data.
        :param event: The event to associate the hardware item with.
        :return: The created hardware item instance.
        """
        hardware_item = form.save(commit=False)
        hardware_item.event = event
        hardware_item.save()
        return hardware_item

    @staticmethod
    def get_hardware_item(hardware_item_id):
        """
        Retrieve a hardware item by its ID.
        :param hardware_item_id: The ID of the hardware item to retrieve.
        :return: The hardware item instance or None if not found.
        """
        return HardwareItem.objects.get(id=hardware_item_id)

    @staticmethod
    def update_hardware_item(form, hardware_item):
        """
        Update an existing hardware item.
        :param form: The form containing the updated hardware item data.
        :param hardware_item: The hardware item instance to update.
        :return: The updated hardware item instance.
        """
        for key, value in form.cleaned_data.items():
            setattr(hardware_item, key, value)

        if form.cleaned_data['image'] is not None:
            if form.cleaned_data['image'] == False:
                hardware_item.image = None

            else:
                hardware_item.image = form.cleaned_data['image']

        else:
            hardware_item.image = hardware_item.image

        hardware_item.save()
        return hardware_item

    @staticmethod
    def delete_hardware_item(hardware_item):
        """
        Delete a hardware item.
        :param hardware_item: The hardware item instance to delete.
        """
        hardware_item.delete()
        return True

    @staticmethod
    def borrow_hardware_item(hardware_item, participant):
        """
        Check if a participant can borrow a hardware item.
        :param hardware_item: The hardware item to check.
        :param participant: The participant trying to borrow the item.
        :return: True if the participant can borrow the item, False otherwise.
        """
        if hardware_item and (not participant in hardware_item.borrowers.all()) and (hardware_item.quantity_available > 0):
            hardware_item.borrowers.add(participant)
            hardware_item.quantity_available -= 1
            hardware_item.save()
            return hardware_item

        return None

    @staticmethod
    def return_hardware_item(hardware_item, participant):
        """
        Return a borrowed hardware item.
        :param hardware_item: The hardware item to return.
        :param participant: The participant returning the item.
        :return: True if the item was successfully returned, False otherwise.
        """
        if hardware_item and participant in hardware_item.borrowers.all():
            hardware_item.borrowers.remove(participant)
            hardware_item.quantity_available += 1
            hardware_item.save()
            return hardware_item

        return False

    @staticmethod
    def hardware_item_to_dict(hardware_item):
        """
        Convert a hardware item to a dictionary representation.
        :param hardware_item: The hardware item to convert.
        :return: A dictionary representation of the hardware item.
        """
        excluded_fields = {
            "id",
            "borrowers",
            "image",
            "event",
        }
        hardware_item_dict = model_to_dict(hardware_item)
        hardware_item_fields = [
            {"name": key, "value": value}
            for key, value in hardware_item_dict.items()
            if key not in excluded_fields
        ]
        return hardware_item_fields
