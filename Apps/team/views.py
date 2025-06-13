import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from Apps.event.services import EventService
from Apps.participant.services import ParticipantService
from Apps.team.forms import TeamForm
from Apps.team.services import TeamService


# Create your views here.
class TeamView(View):
    """
    View to handle the list of teams.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to list all teams.
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

        if ParticipantService.is_user_admin(event, request.user):
            teams = TeamService.get_all_teams(event_id)

            if search:
                teams = TeamService.filter_by_name_or_id(event_id, search, teams)

            return render(request, "teams.html", {"teams": teams})

        team = TeamService.get_team_by_event_and_participant(event, participant)

        if team is None:
            return redirect("/event/" + event_id + "/team/create/")

        form = TeamForm(instance=team)
        participants = TeamService.get_team_participants(team)
        return redirect(f"/event/{event_id}/team/{team.id}/")

class TeamCreateView(View):
    """
    View to handle the creation of a new team.
    """

    def get(self, request, *args, **kwargs):
        """
        Display the team creation form.
        """
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

        if ParticipantService.is_user_admin(event, request.user):
            return redirect("/event/" + event_id + "/team/")

        team = TeamService.get_team_by_event_and_participant(event, participant)

        if team:
            return redirect("/event/" + event_id + "/team/" + str(team.id) + "/")

        form = TeamForm()
        return render(request, "teamCreate.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """
        Handle the submission of the team creation form.
        """
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

        if ParticipantService.is_user_admin(event, request.user):
            return redirect("/event/" + event_id + "/team/")

        team = TeamService.get_team_by_event_and_participant(event, participant)

        if team:
            return redirect("/event/" + event_id + "/team/" + str(team.id) + "/")

        form = TeamForm(request.POST)

        if form.is_valid():
            team = TeamService.create_team(form, event, participant)
            return redirect("/event/" + event_id + "/team/" + str(team.id) + "/")

        return render(request, "teamCreate.html", {"form": form}, status=400)

class TeamCRUDView(View):
    """
    View to handle CRUD operations for a team.
    """

    def get(self, request, *args, **kwargs):
        """
        This view handles the load of an event
        """
        event_id = kwargs.get("event_id")
        team_id = kwargs.get("pk")

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

        team = TeamService.get_team(team_id)

        if team is None:
            return HttpResponse(status=404)

        if ParticipantService.is_user_admin(event, request.user):
            fields = TeamService.team_to_dict(team)
            participants = TeamService.get_team_participants(team)
            return render(request, "teamDetail.html", {"fields": fields, "participants": participants})

        if team and team.members.filter(id=participant.id).exists():
            form = TeamForm(instance=team)
            participants = TeamService.get_team_participants(team)
            return render(request, "teamEdit.html", {"form": form, "participants": participants})

        return redirect("/event/" + event_id + "/team/")

    def post(self, request, *args, **kwargs):
        """
        This view handles the update of a team.
        """
        event_id = kwargs.get("event_id")
        team_id = kwargs.get("pk")

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

        if ParticipantService.is_user_admin(event, request.user):
            return redirect("/event/" + event_id + "/team/")

        team = TeamService.get_team(team_id)

        if team and team.members.filter(id=participant.id).exists():

            form = TeamForm(request.POST, instance=team)

            if form.is_valid():
                TeamService.update_team(team, form.cleaned_data)
                return render(request, "teamEdit.html", {"form": form, "confirmation": "Team updated successfully!"}, status=200)

            else:
                return render(request, "teamEdit.html", {"form": form}, status=400)

        else:
            return redirect("/event/" + event_id + "/team/create/")

    def delete(self, request, *args, **kwargs):
        """
        This view handles the deletion of a team or exit of a team member
        """
        event_id = kwargs.get("event_id")
        team_id = kwargs.get("pk")

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

        team = TeamService.get_team(team_id)

        if team is None:
            return HttpResponse(status=404)

        if team and team.members.filter(id=participant.id).exists():
            team = TeamService.delete_member(team, participant)

            if team.members.count() == 0:
                TeamService.delete_team(team)

        return HttpResponse(status=204)


class TeamJoinView(View):
    """
    View to handle joining a team.
    """

    def get(self, request, *args, **kwargs):
        """
        Handles the rendering of the join team form.
        """
        event_id = kwargs.get("event_id")
        try:
            event = EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if ParticipantService.is_user_admin(event, request.user):
            return redirect("/event/" + event_id + "/team/")

        participant = ParticipantService.get_participant_by_event_and_user(
            event, request.user
        )

        if participant is None:
            return redirect("/event/" + event_id + "/participant/apply/")

        if TeamService.get_team_by_event_and_participant(event, participant):
            return redirect("/event/" + event_id + "/team/")

        return render(request, "teamJoin.html")

    def post(self, request, *args, **kwargs):
        """
        Handle the submission of the join team form.
        """
        event_id = kwargs.get("event_id")

        try:
            event = EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)
        
        try:
            qr = json.loads(request.body).get("qrResult")
        except:
            return HttpResponse(status=400)

        if request.user.is_authenticated is False:
            return HttpResponse(status=401)
        
        if ParticipantService.is_user_admin(event, request.user):
            return redirect("/event/" + event_id + "/team/")

        participant = ParticipantService.get_participant_by_event_and_user(
            event, request.user
        )
        team = TeamService.get_team(qr)

        if not participant or not team:
            return HttpResponse(status=404)

        if TeamService.get_team_by_event_and_participant(event, participant):
            return HttpResponse(status=409)

        if TeamService.add_member(team, participant):
            return HttpResponse(status=200)

        else:
            return HttpResponse(status=409)

class TeamIdView(View):
    """
    This view handles the team id. in a QR format
    """

    def get(self, request, *args, **kwargs):
        """
        This method handles the load of the a specific team id.
        """
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

        if ParticipantService.is_user_admin(event, request.user):
            return redirect("/event/" + event_id + "/team/")

        team = TeamService.get_team_by_event_and_participant(event, participant)

        if team is None:
            return redirect("/event/" + event_id + "/team/create/")

        return render(request, "teamId.html", {"team_id": team.id})
