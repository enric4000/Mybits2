from Apps.project.models import Project, Valoration


class ProjectService():
    """
    Service class for handling project-related operations.
    """

    @staticmethod
    def create_project(form, team):
        """
        Create a new project based on the provided form data, team, and event.
        """
        existing_project = ProjectService.get_projects_by_team(team)
        if existing_project is None:
            project = form.save(commit=False)
            project.team = team
            project.save()
            return project

        else:
            return existing_project

    @staticmethod
    def get_project(project_id):
        """
        Retrieve a project by its ID.
        """
        try:
            project = Project.objects.get(id=project_id)
            return project
        except Project.DoesNotExist:
            raise ValueError(f"Project with id {project_id} does not exist.")

    @staticmethod
    def get_projects_by_team(team):
        """
        Retrieve all projects associated with a specific team.
        """
        project = Project.objects.filter(team=team).first()
        if project:
            project.valoration = ValorationService.get_mean_valoration(project)

        return project

    @staticmethod
    def get_projects(event):
        """
        Retrieve all projects associated with a specific event.
        """
        projects = Project.objects.filter(team__event=event)

        for project in projects:
            project.valoration = ValorationService.get_mean_valoration(project)

        return projects

    @staticmethod
    def search_projects(event, query):
        """
        Search for projects within an event based on a query string.
        """
        projects = Project.objects.filter(
            team__event=event,
            name__icontains=query
        ).distinct()

        for project in projects:
            project.valoration = ValorationService.get_mean_valoration(project)
    
        return projects

    @staticmethod
    def delete_project(project):
        """
        Delete a project.
        """
        project.delete()
        return True

    @staticmethod
    def project_to_dict(project):
        """
        Convert a project instance to a dictionary representation.
        """
        valoration = ValorationService.get_mean_valoration(project)

        return [
            {'name': 'name', 'value': project.name},
            {'name': 'description', 'value': project.description},
            {'name': 'github link', 'value': project.github_link},
            {'name': 'devpost link', 'value': project.devpost_link},
            {'name': 'team name', 'value': project.team.name},
            {'name': 'valoration', 'value': valoration}
        ]

    @staticmethod
    def update_project(form, project):
        """
        Update an existing project with the provided form data.
        """
        for key, value in form.cleaned_data.items():
            setattr(project, key, value)
        project.save()
        return project

class ValorationService():
    """
    Service class for handling project valuation-related operations.
    """

    @staticmethod
    def create_valoration(form, project, admin):
        """
        Create a new valoration for a project by an admin.
        """
        valoration = form.save(commit=False)
        valoration.project = project
        valoration.admin = admin
        valoration.save()
        return valoration

    @staticmethod
    def get_mean_valoration(project):
        """
        Calculate the mean valoration for a project.
        """
        valorations = Valoration.objects.filter(project=project)
        if not valorations:
            return '-'
        return str(sum(val.score for val in valorations) / valorations.count())