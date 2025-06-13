import uuid
from django.db.models import Q
from Apps.activity import models
from Apps.activity.models import Activity
from Apps.participant.models import Hacker, Mentor, Sponsor, Volunteer, Admin


class ActivityService:
    """
    This class handles the operations on the activity model.
    """

    @staticmethod
    def get_activity(activity_id):
        return Activity.objects.filter(id=activity_id).first()

    @staticmethod
    def get_all_activities(event):
        """
        Retrieve all activities associated with a specific event.
        """
        return Activity.objects.filter(event=event)

    @staticmethod
    def filter_by_name_or_id(activities, search):
        """
        Filter activities by name or ID based on the search term.
        """
        return_activities = activities.filter(Q(name__icontains=search))

        try:
            uuid.UUID(str(search))
            return_activities = return_activities | activities.filter(
                Q(id=search)
            )

        except (ValueError, TypeError, AttributeError):
            pass

        return return_activities

    @staticmethod
    def filter_by_type(activities, activity_type):
        """
        Filter activities by type.
        """
        if activities is None:
            return None

        return [
            a for a in activities if a.type.upper() == activity_type.upper()
        ]

    @staticmethod
    def create_activity(form, event):
        """
        Create a new activity based on the provided form data.
        """
        activity = form.save(commit=False)
        activity.event = event
        activity.save()
        return activity

    @staticmethod
    def update_activity(activity, updated_data):
        """
        Update an existing activity with the provided form data.
        """
        for key, value in updated_data.items():
            setattr(activity, key, value)

        activity.save()
        return activity

    @staticmethod
    def delete_activity(activity):
        """
        Delete an existing activity.
        """
        if activity:
            activity.delete()
            return True
        return False

    @staticmethod
    def checkin_participant(activity, participant):
        """
        Check in a participant to an activity.
        """
        added = False
        if (
            isinstance(participant, Hacker)
            and not activity.hacker_participants.filter(id=participant.id).exists()
        ):
            activity.hacker_participants.add(participant)
            added = True

        elif (
            isinstance(participant, Mentor)
            and not activity.mentor_participants.filter(id=participant.id).exists()
        ):
            activity.mentor_participants.add(participant)
            added = True

        elif (
            isinstance(participant, Sponsor)
            and not activity.sponsor_participants.filter(id=participant.id).exists()
        ):
            activity.sponsor_participants.add(participant)
            added = True

        elif (
            isinstance(participant, Volunteer)
            and not activity.volunteer_participants.filter(id=participant.id).exists()
        ):
            activity.volunteer_participants.add(participant)
            added = True

        elif (
            isinstance(participant, Admin)
            and not activity.admin_participants.filter(id=participant.id).exists()
        ):
            activity.admin_participants.add(participant)
            added = True

        activity.save()
        return added

    @staticmethod
    def get_participant_count(activity):
        """
        Get the count of participants in an activity.
        """

        count = activity.hacker_participants.all().count()
        count = count + activity.mentor_participants.all().count()
        count = count + activity.sponsor_participants.all().count()
        count = count + activity.volunteer_participants.all().count()
        count = count + activity.admin_participants.all().count()
        return count
