from django.db.models import Q
from django.utils.timezone import now
from .models import Event


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
        return Event.objects.delete(event_id)

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

        if event.hacker_deadline < now():
            opened_applications.update(
                {
                    "hacker_applications": True,
                }
            )

        if event.mentor_deadline < now():
            opened_applications.update(
                {
                    "mentor_applications": True,
                }
            )

        if event.sponsor_deadline < now():
            opened_applications.update(
                {
                    "sponsor_applications": True,
                }
            )

        if event.volunteer_deadline < now():
            opened_applications.update(
                {
                    "volunteer_applications": True,
                }
            )

        return opened_applications

    @staticmethod
    def is_hacker_deadline_valid(event):
        return event.hacker_deadline < now() and event.end_date > event.hacker_deadline

    @staticmethod
    def is_mentor_deadline_valid(event):
        return event.mentor_deadline < now() and event.end_date > event.mentor_deadline

    @staticmethod
    def is_sponsor_deadline_valid(event):
        return (
            event.sponsor_deadline < now() and event.end_date > event.sponsor_deadline
        )

    @staticmethod
    def is_volunteer_deadline_valid(event):
        return (
            event.volunteer_deadline < now()
            and event.end_date > event.volunteer_deadline
        )
