from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from Apps.event.services import EventService
from Apps.participant.services import ParticipantService
from Apps.project.forms import ProjectForm, ValorationForm
from Apps.project.services import ProjectService, ValorationService
from Apps.team.services import TeamService

# Create your views here.
class ProjectView(View):
    """
    View for handling the list of projects.
    """
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to list all projects.
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
            participant = ParticipantService.get_participant_by_event_and_user(event, request.user)
            team = TeamService.get_team_by_event_and_participant(event, participant)

            if not participant:
                return HttpResponse(status=403)

            if not team:
                return redirect(f"/event/{event_id}/team/create/")
            
            project = ProjectService.get_projects_by_team(team)

            if not project:
                return redirect(f"/event/{event_id}/project/create/")
            
            return redirect(f"/event/{event_id}/project/{project.id}/")

        if search:
            projects = ProjectService.search_projects(event, search)

        else:
            projects = ProjectService.get_projects(event)

        return render(request, 'projects.html', {'projects': projects})

class ProjectCreateView(View):
    """
    View for handling the creation of a new project.
    """
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to render the project creation form.
        """
        event_id = kwargs.get("event_id")
        try:
            event = EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if ParticipantService.is_user_admin(event, request.user):
            return redirect(f"/event/{event_id}/project/")

        participant = ParticipantService.get_participant_by_event_and_user(event, request.user)
        team = TeamService.get_team_by_event_and_participant(event, participant)

        if not participant:
            return HttpResponse(status=403)

        if not team:
            return redirect(f"/event/{event_id}/team/create/")

        project = ProjectService.get_projects_by_team(team)

        if project:
            return redirect(f"/event/{event_id}/project/{project.id}/")

        form = ProjectForm()
        return render(request, 'projectCreate.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a new project.
        """
        event_id = kwargs.get("event_id")
        try:
            event = EventService.get_event(event_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if ParticipantService.is_user_admin(event, request.user):
            return redirect(f"/event/{event_id}/project/")

        participant = ParticipantService.get_participant_by_event_and_user(event, request.user)
        team = TeamService.get_team_by_event_and_participant(event, participant)

        if not participant or not team:
            return HttpResponse(status=403)

        form = ProjectForm(request.POST)

        if form.is_valid():
            project = ProjectService.create_project(form, team)
            return redirect(f"/event/{event_id}/project/{project.id}/")
        
        return render(request, 'projectCreate.html', {'form': form}, status=400)
    
class ProjectCRUDView(View):
    """
    View for handling the CRUD operations of a project.
    """
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to view a specific project.
        """
        event_id = kwargs.get("event_id")
        project_id = kwargs.get("pk")

        try:
            event = EventService.get_event(event_id)
            project = ProjectService.get_project(project_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if ParticipantService.is_user_admin(event, request.user):
            project_dict = ProjectService.project_to_dict(project)
            return render(request, 'projectDetail.html', {'fields': project_dict})

        participant = ParticipantService.get_participant_by_event_and_user(event, request.user)
        team = TeamService.get_team_by_event_and_participant(event, participant)

        if not participant:
            return HttpResponse(status=403)
        
        if not team:
            return redirect(f"/event/{event_id}/team/create/")
        
        if team != project.team:
            return HttpResponse(status=403)
        
        form = ProjectForm(instance=project)
        return render(request, 'projectEdit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to update a specific project.
        """
        event_id = kwargs.get("event_id")
        project_id = kwargs.get("pk")

        try:
            event = EventService.get_event(event_id)
            project = ProjectService.get_project(project_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if ParticipantService.is_user_admin(event, request.user):
            return redirect(f"/event/{event_id}/project/")

        participant = ParticipantService.get_participant_by_event_and_user(event, request.user)
        team = TeamService.get_team_by_event_and_participant(event, participant)

        if not participant:
            return HttpResponse(status=403)

        if not team:
            return redirect(f"/event/{event_id}/team/create/")

        if team != project.team:
            return HttpResponse(status=403)

        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            updated_project = ProjectService.update_project(form, project)
            return render(request, 'projectEdit.html', {'form': form, 'confirmation': "Project updated successfully!"})

        return render(request, 'projectEdit.html', {'form': form}, status=400)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE request to delete a specific project.
        """
        event_id = kwargs.get("event_id")
        project_id = kwargs.get("pk")

        try:
            event = EventService.get_event(event_id)
            project = ProjectService.get_project(project_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if ParticipantService.is_user_admin(event, request.user):
            return redirect(f"/event/{event_id}/project/")

        participant = ParticipantService.get_participant_by_event_and_user(event, request.user)
        team = TeamService.get_team_by_event_and_participant(event, participant)

        if not participant:
            return HttpResponse(status=403)

        if not team:
            return redirect(f"/event/{event_id}/team/create/")

        if team != project.team:
            return HttpResponse(status=403)

        ProjectService.delete_project(project)
        return HttpResponse(status=204)

class ProjectValorationView(View):
    """
    View for handling the valoration of a project by an admin.
    """
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to valorate a project.
        """
        event_id = kwargs.get("event_id")
        project_id = kwargs.get("pk")

        try:
            event = EventService.get_event(event_id)
            project = ProjectService.get_project(project_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        form = ValorationForm()
        return render(request, 'projectValoration.html', {'form': form, 'project': project})

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to valorate a project.
        """
        event_id = kwargs.get("event_id")
        project_id = kwargs.get("pk")

        try:
            event = EventService.get_event(event_id)
            project = ProjectService.get_project(project_id)

        except ValueError:
            return HttpResponse(status=404)

        if request.user.is_authenticated is False:
            return redirect("/user/login/?next=" + request.path)

        if not ParticipantService.is_user_admin(event, request.user):
            return HttpResponse(status=403)

        admin = ParticipantService.get_participant_by_event_and_user(event, request.user)

        form = ValorationForm(request.POST)
        if form.is_valid():
            valoration = ValorationService.create_valoration(form, project, admin)
            return redirect(f"/event/{event_id}/project/{project.id}/")

        return render(request, 'projectValoration.html', {'form': form}, status=400)
