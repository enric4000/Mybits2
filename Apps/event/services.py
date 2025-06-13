from django.db.models import Q
from django.forms import model_to_dict
from django.utils.timezone import now
from .models import Event
from .Enums.timezoneEnum import TimezoneEnum  # Adjust the import path as needed


class EventService:
    @staticmethod
    def create_event(form):
        event = form.save(commit=False)
        event.save()
        return event

    @staticmethod
    def get_event(event_id):
        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise ValueError("Event not found")

    @staticmethod
    def update_event(event_id, updated_data):
        event = Event.objects.get(id=event_id)
        for key, value in updated_data.items():
            setattr(event, key, value)
        event.save()
        return event

    @staticmethod
    def delete_event(event_id):
        event = EventService.get_event(event_id)
        return event.delete()

    @staticmethod
    def get_first_100_events():
        """
        Retrieve the first 100 events from the database.
        """
        events = Event.objects.all()[:100]
        return events

    @staticmethod
    def find_by_name_and_appName(search):
        """
        Retrieve events by name or appName.
        """
        events = Event.objects.filter(
            Q(name__icontains=search) | Q(AppName__icontains=search)
        )
        return events

    @staticmethod
    def get_opened_applications(event_id):
        """
        This method returns the list of opened applications for a specific event.
        """
        event = EventService.get_event(event_id)
        opened_applications = {
            "hacker_applications": False,
            "mentor_applications": False,
            "sponsor_applications": False,
            "volunteer_applications": False,
        }

        if event.end_date < now():
            return opened_applications

        if event.hacker_deadline > now():
            opened_applications.update(
                {
                    "hacker_applications": True,
                }
            )

        if event.mentor_deadline > now():
            opened_applications.update(
                {
                    "mentor_applications": True,
                }
            )

        if event.sponsor_deadline > now():
            opened_applications.update(
                {
                    "sponsor_applications": True,
                }
            )

        if event.volunteer_deadline > now():
            opened_applications.update(
                {
                    "volunteer_applications": True,
                }
            )

        return opened_applications

    @staticmethod
    def event_to_dict(event):
        """
        Convert an event instance to a dictionary.
        """
        excluded_fields = {
            "hacker_deadline",
            "mentor_deadline",
            "sponsor_deadline",
            "volunteer_deadline",
            "activities_enabled",
            "warehouse_enabled",
            "hardware_enabled",
            "judging_enabled",
        }
        event_dict = model_to_dict(event)
        event_fields = [
            {"name": key, "value": value}
            for key, value in event_dict.items()
            if key not in excluded_fields
        ]
        timezone_value = TimezoneEnum[event.timezone].value
        for field in event_fields:
            if field["name"] == "timezone":
                field["value"] = timezone_value
                break

        return event_fields
