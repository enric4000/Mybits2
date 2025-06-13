import uuid
from django.forms import model_to_dict
from Apps.team.models import Team
from django.db import models


class TeamService:
    """
    Service class to handle team-related operations.
    """

    @staticmethod
    def create_team(form, event, participant):
        """
        Create a new team based on the provided form data.
        """
        team = form.save(commit=False)
        team.event = event
        team.save()
        team.members.add(participant)
        team.save()
        return team

    @staticmethod
    def get_team_by_event_and_participant(event, participant):
        """
        Retrieve the team associated with a specific event and participant.
        """
        return Team.objects.filter(event=event, members__in=[participant]).first()

    @staticmethod
    def get_all_teams(event):
        """
        Retrieve all teams associated with a specific event.
        """
        return Team.objects.filter(event=event)

    @staticmethod
    def filter_by_name_or_id(event, search_term, teams):
        """
        Filter teams by name or ID based on the search term.
        """
        return_teams = teams.filter(models.Q(name__icontains=search_term))

        try:
            uuid.UUID(str(search_term))
            return_teams = return_teams | teams.filter(models.Q(id=search_term))

        except (ValueError, TypeError, AttributeError):
            pass

        return return_teams

    @staticmethod
    def get_team(team_id):
        """
        Retrieve a team by its ID.
        """
        return Team.objects.filter(id=team_id).first()

    @staticmethod
    def update_team(team, data):
        """
        Update an existing team with the provided data.
        """
        if team:
            for key, value in data.items():
                setattr(team, key, value)
            team.save()
            return team

        return None

    @staticmethod
    def add_member(team, participant):
        """
        Add a participant to a team.
        """
        if team and not participant in team.members.all():
            team.members.add(participant)
            team.save()
            return team

        return None

    @staticmethod
    def delete_member(team, participant):
        """
        Remove a participant from a team.
        """
        if team and participant in team.members.all():
            team.members.remove(participant)
            team.save()
            return team

        return None

    @staticmethod
    def get_team_participants(team):
        """
        Delete a team by its ID.
        """
        dict = []
        for member in team.members.all():
            dict.append({"name": "members", "value": member.user.first_name})
        return dict

    @staticmethod
    def delete_team(team):
        """
        Delete a team
        """
        if team:
            team.delete()
            return True
        return False

    @staticmethod
    def team_to_dict(team):
        team_dict = model_to_dict(team)
        dict = [{"name": "name", "value": team.name}]
        return dict
