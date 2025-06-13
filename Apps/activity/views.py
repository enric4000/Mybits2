import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from Apps.activity.forms import ActivityForm
from Apps.activity.services import ActivityService
from Apps.event.services import EventService
from Apps.participant.services import ParticipantService

# Create your views here.
class ActivityView(View):
    """
    View to handle the list of activities.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to list all activities.
        """
        search = request.GET.get("search")
        event_id = kwargs.get("event_id")
        activity_type = request.GET.get("type")
        
        try:
            event = EventService.get_event(event_id)
    
        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return redirect("/event/" + str(event_id) + "/")

        activities = ActivityService.get_all_activities(event)

        if search:
            activities = ActivityService.filter_by_name_or_id(activities, search)

        if activity_type:
            activities = ActivityService.filter_by_type(activities, activity_type)

        return render(request, "activities.html", {"activities": activities})


class ActivityCreateView(View):
    """
    View to handle the creation of a new activity.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to display the activity creation form.
        """
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
    
        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return redirect("/event/" + str(event_id) + "/")

        form = ActivityForm()
        return render(request, "activityCreate.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new activity.
        """
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
    
        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return redirect("/event/" + str(event_id) + "/")

        form = ActivityForm(request.POST)
        if form.is_valid():
            ActivityService.create_activity(form, event)
            return redirect("/event/" + str(event_id) + "/activity/")

        return render(request, "activityCreate.html", {"form": form}, status=400)


class ActivityCRUDView(View):
    """
    View to handle CRUD operations for activities.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to display the activity details.
        """
        activity_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
    
        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return redirect("/event/" + str(event_id) + "/")

        activity = ActivityService.get_activity(activity_id)

        if not activity:
            return redirect("/event/" + str(event_id) + "/activity/")

        form = ActivityForm(instance=activity)
        count = ActivityService.get_participant_count(activity)
        return render(request, "activityEdit.html", {"form": form, "count": count})

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to update an activity.
        """
        activity_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
            activity = ActivityService.get_activity(activity_id)
    
        except ValueError:
            return HttpResponse(status=404)
        
        if not activity:
            return redirect("/event/" + str(event_id) + "/activity/")

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return redirect("/event/" + str(event_id) + "/")

        form = ActivityForm(request.POST)

        if form.is_valid():
            ActivityService.update_activity(activity, form.cleaned_data)
            return render(
                request,
                "activityEdit.html",
                {"form": form, "confirmation": "Activity updated successfully."},
            )

        return render(request, "activityEdit.html", {"form": form}, status=400)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests to remove an activity.
        """
        activity_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)
            activity = ActivityService.get_activity(activity_id)

        except ValueError:
            return HttpResponse(status=404)

        if not activity:
            return redirect("/event/" + str(event_id) + "/activity/")

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return redirect("/event/" + str(event_id) + "/")

        if ActivityService.delete_activity(activity):
            return HttpResponse(status=204)

        return HttpResponse(status=400)


class ActivityCheckinView(View):
    """
    View to handle the check-in process for activities.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to display the check-in form.
        """
        activity_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")
        
        try:
            event = EventService.get_event(event_id)
            activity = ActivityService.get_activity(activity_id)

        except ValueError:
            return HttpResponse(status=404)

        if not activity:
            return redirect("/event/" + str(event_id) + "/activity/")
        
        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return redirect("/event/" + str(event_id) + "/")

        return render(request, "activityCheckIn.html")

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to check in a participant to an activity.
        """
        activity_id = kwargs.get("pk")
        event_id = kwargs.get("event_id")
        try:
            event = EventService.get_event(event_id)
            qr = json.loads(request.body).get("qrResult")
            activity = ActivityService.get_activity(activity_id)
            participant = ParticipantService.get_participant(event_id, qr)

        except ValueError:
            return HttpResponse(status=404)

        if not activity or not participant:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return HttpResponse(status=401)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)
        
        result = ActivityService.checkin_participant(activity, participant)
        diet = ParticipantService.get_participant_diet(participant)
        if not result:
            return HttpResponse(status=409, content=json.dumps({"diet": diet}))

        return HttpResponse(status=200, content=json.dumps({"diet": diet}))
