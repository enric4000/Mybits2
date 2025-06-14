from django.forms import ValidationError
from django.test import TestCase

from Apps.event.models import Event
from Apps.participant.models import Admin, Hacker
from Apps.project.forms import ProjectForm, ValorationForm
from Apps.project.models import Project, Valoration
from Apps.project.services import ProjectService, ValorationService
from Apps.team.models import Team
from Apps.users.models import CustomUser

# Create your tests here.
class ModelProjectTestCase(TestCase):
    def setUp(self):
        self.event = Event(
            name="Service Test Event",
            AppName="ServiceTestApp",
            description="This is a service test event.",
            location="Service Test Location",
            timezone="UTC",
            start_date="2023-10-01T09:00:00Z",
            end_date="2023-10-02T18:00:00Z",
            hacker_deadline="2023-09-25T23:59:59Z",
            mentor_deadline="2023-09-26T23:59:59Z",
            volunteer_deadline="2023-09-27T23:59:59Z",
            sponsor_deadline="2023-09-28T23:59:59Z",
            terms_and_conditions_link="https://example.com/terms",
        )
        self.event.save()
        self.user1 = CustomUser(
            email="a@a.com",
            password="123456AA!a",
            username="albert",
            first_name="albert",
            last_name="a",
            gender="MALE",
            gender_other="",
            pronoun="he/him",
            date_of_birth="2000-01-01",
            dietary="NONE",
            dietary_other="",
            origin="Spain",
        )

        self.user1_password = self.user1.password
        self.user1.set_password(self.user1_password)
        self.user1.save()

        self.hacker_data = {
            "accepted_date":None,
            "application_date":"2000-01-01",
            "phone_number":"+1234567890",
            "type":"Hacker",
            "accepted_terms_and_conditions":True,
            "t_shirt_size":"M",
            "origin":"Spain",
            "status":"Under Review",
            "university":"Test University",
            "degree":"Computer Science",
            "graduation_year":2024,
            "under_age":False,
            "lenny_face":"( ͡° ͜ʖ ͡°)",
            "hear_about_us":"From a friend",
            "why_excited":"I love coding and innovation!",
            "first_hackathon":True,
            "personal_projects":"My personal projects include a weather app and a portfolio website.",
            "share_cv":True,
            "subscribe":True,
        }

        self.hacker = Hacker(
            **self.hacker_data,
            event=self.event,
            user=self.user1,
        )
        self.hacker.save()

        self.team = Team(
            name="Test Team",
            event=self.event,
        )
        self.team.save()
        self.team.members.add(self.hacker)
        self.team.save()

        self.user2 = CustomUser.objects.create(
            email="b@b.com",
            password="123456AA!a",
            username="bb",
            first_name="bb",
            last_name="b",
            gender="MALE",
            gender_other="",
            pronoun="he/him",
            date_of_birth="2000-01-01",
            dietary="NONE",
            dietary_other="",
            origin="Spain",
        )

        self.user2_password = self.user2.password
        self.user2.set_password(self.user2_password)
        self.user2.save()

        self.admin = Admin(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user2,
        )
        self.admin.save()

    def test_project_creation(self):
        project = Project(
            name="Test Project",
            description="This is a test project.",
            github_link="http://example.com/",
            devpost_link="http://example.com/",
            team=self.team,
        )
        project.save()

        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.description, "This is a test project.")
        self.assertEqual(project.github_link, "http://example.com/")
        self.assertEqual(project.devpost_link, "http://example.com/")
        self.assertEqual(project.team, self.team)

    def test_project_incorrect_data_creation(self):
        with self.assertRaises(Exception):
            project = Project(
                name="",
                description="This is a test project.",
                github_link="example",
                devpost_link="com/",
            )
            project.save()

    def test_valoration_creation(self):
        project = Project(
            name="Test Project",
            description="This is a test project.",
            github_link="http://example.com/",
            devpost_link="http://example.com/",
            team=self.team,
        )
        project.save()
        
        valoration = Valoration(
            score=8,
            project=project,
            admin=self.admin,
        )
        valoration.clean()
        valoration.save()

        self.assertEqual(valoration.score, 8)
        self.assertEqual(valoration.project, project)
        self.assertEqual(valoration.admin, self.admin)

    def test_valoration_incorrect_data_creation(self):
        project = Project(
            name="Test Project",
            description="This is a test project.",
            github_link="http://example.com/",
            devpost_link="http://example.com/",
            team=self.team,
        )
        project.save()

        with self.assertRaises(ValidationError):
            valoration = Valoration(
                score=11,  # Invalid score
                project=project,
                admin=self.admin,
            )
            valoration.clean()
            valoration.save()

class ServiceProjectTestCase(TestCase):
    def setUp(self):
        self.event = Event(
            name="Service Test Event",
            AppName="ServiceTestApp",
            description="This is a service test event.",
            location="Service Test Location",
            timezone="UTC",
            start_date="2023-10-01T09:00:00Z",
            end_date="2023-10-02T18:00:00Z",
            hacker_deadline="2023-09-25T23:59:59Z",
            mentor_deadline="2023-09-26T23:59:59Z",
            volunteer_deadline="2023-09-27T23:59:59Z",
            sponsor_deadline="2023-09-28T23:59:59Z",
            terms_and_conditions_link="https://example.com/terms",
        )
        self.event.save()
        self.event2 = Event(
            name="Service Test Event 2",
            AppName="ServiceTestApp2",
            description="This is another service test event.",
            location="Service Test Location 2",
            timezone="UTC",
            start_date="2023-11-01T09:00:00Z",
            end_date="2023-11-02T18:00:00Z",
            hacker_deadline="2023-10-25T23:59:59Z",
            mentor_deadline="2023-10-26T23:59:59Z",
            volunteer_deadline="2023-10-27T23:59:59Z",
            sponsor_deadline="2023-10-28T23:59:59Z",
            terms_and_conditions_link="https://example.com/terms2",
        )
        self.event2.save()
        self.user1 = CustomUser(
            email="a@a.com",
            password="123456AA!a",
            username="albert",
            first_name="albert",
            last_name="a",
            gender="MALE",
            gender_other="",
            pronoun="he/him",
            date_of_birth="2000-01-01",
            dietary="NONE",
            dietary_other="",
            origin="Spain",
        )

        self.user1_password = self.user1.password
        self.user1.set_password(self.user1_password)
        self.user1.save()

        self.hacker_data = {
            "accepted_date":None,
            "application_date":"2000-01-01",
            "phone_number":"+1234567890",
            "type":"Hacker",
            "accepted_terms_and_conditions":True,
            "t_shirt_size":"M",
            "origin":"Spain",
            "status":"Under Review",
            "university":"Test University",
            "degree":"Computer Science",
            "graduation_year":2024,
            "under_age":False,
            "lenny_face":"( ͡° ͜ʖ ͡°)",
            "hear_about_us":"From a friend",
            "why_excited":"I love coding and innovation!",
            "first_hackathon":True,
            "personal_projects":"My personal projects include a weather app and a portfolio website.",
            "share_cv":True,
            "subscribe":True,
        }

        self.hacker = Hacker(
            **self.hacker_data,
            event=self.event,
            user=self.user1,
        )
        self.hacker.save()

        self.team = Team(
            name="Test Team",
            event=self.event,
        )
        self.team.save()
        self.team.members.add(self.hacker)
        self.team.save()

        self.user2 = CustomUser.objects.create(
            email="b@b.com",
            password="123456AA!a",
            username="bb",
            first_name="bb",
            last_name="b",
            gender="MALE",
            gender_other="",
            pronoun="he/him",
            date_of_birth="2000-01-01",
            dietary="NONE",
            dietary_other="",
            origin="Spain",
        )

        self.user2_password = self.user2.password
        self.user2.set_password(self.user2_password)
        self.user2.save()

        self.admin = Admin(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user2,
        )
        self.admin.save()

        self.project_data = {
            "name": "Test Project",
            "description": "This is a test project.",
            "github_link": "http://example.com/",
            "devpost_link": "http://example.com/",
        }

        self.valoration_data = {
            "score":8,
        }

    def test_create_project(self):
        """
        Test creating a project with valid data.
        """
        form = ProjectForm(self.project_data)
        form.is_valid()
        
        project = ProjectService.create_project(form, self.team)
        self.assertIsInstance(project, Project)
        self.assertEqual(project.name, self.project_data["name"])
        self.assertEqual(project.description, self.project_data["description"])
        self.assertEqual(project.github_link, self.project_data["github_link"])
        self.assertEqual(project.devpost_link, self.project_data["devpost_link"])
        self.assertEqual(project.team, self.team)

        existing_project = ProjectService.create_project(form, self.team)
        self.assertEqual(existing_project, project)

    def test_get_project(self):
        """
        Test retrieving a project by its ID.
        """
        project = Project(**self.project_data, team=self.team)
        project.save()

        retrieved_project = ProjectService.get_project(project.id)
        self.assertEqual(retrieved_project, project)
        with self.assertRaises(ValueError):
            ProjectService.get_project(9999)

    def test_get_projects_by_team(self):
        """
        Test retrieving projects by team.
        """
        project1 = Project(**self.project_data, team=self.team)
        project1.save()

        team2 = Team(
            name="Another Team",
            event=self.event2,
        )
        team2.save()
        projects = ProjectService.get_projects_by_team(self.team)
        project2 = ProjectService.get_projects_by_team(team2)

        self.assertEqual(project1, projects)
        self.assertIsNone(project2)

    def test_get_projects_by_event(self):
        """
        Test retrieving all projects associated with an event.
        """
        project1 = Project(**self.project_data, team=self.team)
        project1.save()
        
        team2 = Team(
            name="Another Team",
            event=self.event2,
        )
        team2.save()
        project2 = Project(
            name="Another Project",
            description="This is another test project.",
            github_link="http://example.com/another",
            devpost_link="http://example.com/another",
            team=team2,
        )
        project2.save()

        projects = ProjectService.get_projects(self.event)
        self.assertIn(project1, projects)
        self.assertNotIn(project2, projects)

    def test_search_projects(self):
        """
        Test searching for projects within an event based on a query string.
        """
        project1 = Project(
            name="Test Project",
            description="This is a test project.",
            github_link="http://example.com/",
            devpost_link="http://example.com/",
            team=self.team,
        )
        project1.save()
        
        project2 = Project(
            name="Another Project",
            description="This is another test project.",
            github_link="http://example.com/another",
            devpost_link="http://example.com/another",
            team=self.team,
        )
        project2.save()

        projects = ProjectService.search_projects(self.event, "Test")
        self.assertIn(project1, projects)
        self.assertNotIn(project2, projects)
        projects = ProjectService.search_projects(self.event, "Another")
        self.assertIn(project2, projects)
        self.assertNotIn(project1, projects)

    def test_delete_project(self):
        """
        Test deleting a project.
        """
        project = Project(**self.project_data, team=self.team)
        project.save()

        result = ProjectService.delete_project(project)
        self.assertTrue(result)

        with self.assertRaises(ValueError):
            ProjectService.get_project(project.id)

    def test_project_to_dict(self):
        """
        Test converting a project instance to a dictionary representation.
        """
        project = Project(**self.project_data, team=self.team)
        project.save()

        project_dict = ProjectService.project_to_dict(project)
        self.assertIsInstance(project_dict, list)
        self.assertEqual(len(project_dict), 6)
        self.assertEqual(project_dict[0]['name'], 'name')
        self.assertEqual(project_dict[0]['value'], project.name)
        self.assertEqual(project_dict[1]['name'], 'description')
        self.assertEqual(project_dict[1]['value'], project.description)
        self.assertEqual(project_dict[2]['name'], 'github link')
        self.assertEqual(project_dict[2]['value'], project.github_link)
        self.assertEqual(project_dict[3]['name'], 'devpost link')
        self.assertEqual(project_dict[3]['value'], project.devpost_link)

    def test_update_project(self):
        """
        Test updating a project with valid data.
        """
        project = Project(**self.project_data, team=self.team)
        project.save()

        updated_data = {
            "name": "Updated Project",
            "description": "This is an updated test project.",
            "github_link": "http://updated-example.com/",
            "devpost_link": "http://updated-example.com/",
        }
        
        form = ProjectForm(updated_data, instance=project)
        form.is_valid()
        
        updated_project = ProjectService.update_project(form, project)
        self.assertEqual(updated_project.name, updated_data["name"])
        self.assertEqual(updated_project.description, updated_data["description"])
        self.assertEqual(updated_project.github_link, updated_data["github_link"])
        self.assertEqual(updated_project.devpost_link, updated_data["devpost_link"])

class ServiceValorationTestCase(TestCase):
    def setUp(self):
        self.event = Event(
            name="Service Test Event",
            AppName="ServiceTestApp",
            description="This is a service test event.",
            location="Service Test Location",
            timezone="UTC",
            start_date="2023-10-01T09:00:00Z",
            end_date="2023-10-02T18:00:00Z",
            hacker_deadline="2023-09-25T23:59:59Z",
            mentor_deadline="2023-09-26T23:59:59Z",
            volunteer_deadline="2023-09-27T23:59:59Z",
            sponsor_deadline="2023-09-28T23:59:59Z",
            terms_and_conditions_link="https://example.com/terms",
        )
        self.event.save()
        self.event2 = Event(
            name="Service Test Event 2",
            AppName="ServiceTestApp2",
            description="This is another service test event.",
            location="Service Test Location 2",
            timezone="UTC",
            start_date="2023-11-01T09:00:00Z",
            end_date="2023-11-02T18:00:00Z",
            hacker_deadline="2023-10-25T23:59:59Z",
            mentor_deadline="2023-10-26T23:59:59Z",
            volunteer_deadline="2023-10-27T23:59:59Z",
            sponsor_deadline="2023-10-28T23:59:59Z",
            terms_and_conditions_link="https://example.com/terms2",
        )
        self.event2.save()
        self.user1 = CustomUser(
            email="a@a.com",
            password="123456AA!a",
            username="albert",
            first_name="albert",
            last_name="a",
            gender="MALE",
            gender_other="",
            pronoun="he/him",
            date_of_birth="2000-01-01",
            dietary="NONE",
            dietary_other="",
            origin="Spain",
        )

        self.user1_password = self.user1.password
        self.user1.set_password(self.user1_password)
        self.user1.save()

        self.hacker_data = {
            "accepted_date":None,
            "application_date":"2000-01-01",
            "phone_number":"+1234567890",
            "type":"Hacker",
            "accepted_terms_and_conditions":True,
            "t_shirt_size":"M",
            "origin":"Spain",
            "status":"Under Review",
            "university":"Test University",
            "degree":"Computer Science",
            "graduation_year":2024,
            "under_age":False,
            "lenny_face":"( ͡° ͜ʖ ͡°)",
            "hear_about_us":"From a friend",
            "why_excited":"I love coding and innovation!",
            "first_hackathon":True,
            "personal_projects":"My personal projects include a weather app and a portfolio website.",
            "share_cv":True,
            "subscribe":True,
        }

        self.hacker = Hacker(
            **self.hacker_data,
            event=self.event,
            user=self.user1,
        )
        self.hacker.save()

        self.team = Team(
            name="Test Team",
            event=self.event,
        )
        self.team.save()
        self.team.members.add(self.hacker)
        self.team.save()

        self.user2 = CustomUser.objects.create(
            email="b@b.com",
            password="123456AA!a",
            username="bb",
            first_name="bb",
            last_name="b",
            gender="MALE",
            gender_other="",
            pronoun="he/him",
            date_of_birth="2000-01-01",
            dietary="NONE",
            dietary_other="",
            origin="Spain",
        )

        self.user2_password = self.user2.password
        self.user2.set_password(self.user2_password)
        self.user2.save()

        self.admin = Admin(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user2,
        )
        self.admin.save()

        self.project_data = {
            "name": "Test Project",
            "description": "This is a test project.",
            "github_link": "http://example.com/",
            "devpost_link": "http://example.com/",
        }

        self.valoration_data = {
            "score":8,
        }

    def test_create_valoration(self):
        """
        Test creating a valoration for a project by an admin.
        """
        project = Project(
            name="Test Project",
            description="This is a test project.",
            github_link="http://example.com/",
            devpost_link="http://example.com/",
            team=self.team,
        )
        project.save()

        form = ValorationForm(self.valoration_data)
        form.is_valid()
        
        valoration = ValorationService.create_valoration(form, project, self.admin)
        self.assertIsInstance(valoration, Valoration)
        self.assertEqual(valoration.score, self.valoration_data["score"])
        self.assertEqual(valoration.project, project)
        self.assertEqual(valoration.admin, self.admin)

    def test_get_mean_valoration(self):
        """
        Test calculating the mean valoration for a project.
        """
        project = Project(
            name="Test Project",
            description="This is a test project.",
            github_link="http://example.com/",
            devpost_link="http://example.com/",
            team=self.team,
        )
        project.save()

        valoration1 = Valoration(
            score=8,
            project=project,
            admin=self.admin,
        )
        valoration1.save()

        valoration2 = Valoration(
            score=6,
            project=project,
            admin=self.admin,
        )
        valoration2.save()

        mean_valoration = ValorationService.get_mean_valoration(project)
        self.assertEqual(mean_valoration, '7.0')

class ViewProjectTestCase(TestCase):
    def setUp(self):
        self.event = Event(
            name="Service Test Event",
            AppName="ServiceTestApp",
            description="This is a service test event.",
            location="Service Test Location",
            timezone="UTC",
            start_date="2023-10-01T09:00:00Z",
            end_date="2023-10-02T18:00:00Z",
            hacker_deadline="2023-09-25T23:59:59Z",
            mentor_deadline="2023-09-26T23:59:59Z",
            volunteer_deadline="2023-09-27T23:59:59Z",
            sponsor_deadline="2023-09-28T23:59:59Z",
            terms_and_conditions_link="https://example.com/terms",
        )
        self.event.save()
        self.event2 = Event(
            name="Service Test Event 2",
            AppName="ServiceTestApp2",
            description="This is another service test event.",
            location="Service Test Location 2",
            timezone="UTC",
            start_date="2023-11-01T09:00:00Z",
            end_date="2023-11-02T18:00:00Z",
            hacker_deadline="2023-10-25T23:59:59Z",
            mentor_deadline="2023-10-26T23:59:59Z",
            volunteer_deadline="2023-10-27T23:59:59Z",
            sponsor_deadline="2023-10-28T23:59:59Z",
            terms_and_conditions_link="https://example.com/terms2",
        )
        self.event2.save()
        self.user1 = CustomUser(
            email="a@a.com",
            password="123456AA!a",
            username="albert",
            first_name="albert",
            last_name="a",
            gender="MALE",
            gender_other="",
            pronoun="he/him",
            date_of_birth="2000-01-01",
            dietary="NONE",
            dietary_other="",
            origin="Spain",
        )

        self.user1_password = self.user1.password
        self.user1.set_password(self.user1_password)
        self.user1.save()

        self.hacker_data = {
            "accepted_date":None,
            "application_date":"2000-01-01",
            "phone_number":"+1234567890",
            "type":"Hacker",
            "accepted_terms_and_conditions":True,
            "t_shirt_size":"M",
            "origin":"Spain",
            "status":"Under Review",
            "university":"Test University",
            "degree":"Computer Science",
            "graduation_year":2024,
            "under_age":False,
            "lenny_face":"( ͡° ͜ʖ ͡°)",
            "hear_about_us":"From a friend",
            "why_excited":"I love coding and innovation!",
            "first_hackathon":True,
            "personal_projects":"My personal projects include a weather app and a portfolio website.",
            "share_cv":True,
            "subscribe":True,
        }

        self.hacker = Hacker(
            **self.hacker_data,
            event=self.event,
            user=self.user1,
        )
        self.hacker.save()

        self.team = Team(
            name="Test Team",
            event=self.event,
        )
        self.team.save()
        self.team.members.add(self.hacker)
        self.team.save()

        self.user2 = CustomUser.objects.create(
            email="b@b.com",
            password="123456AA!a",
            username="bb",
            first_name="bb",
            last_name="b",
            gender="MALE",
            gender_other="",
            pronoun="he/him",
            date_of_birth="2000-01-01",
            dietary="NONE",
            dietary_other="",
            origin="Spain",
        )

        self.user2_password = self.user2.password
        self.user2.set_password(self.user2_password)
        self.user2.save()

        self.admin = Admin(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user2,
        )

        self.project_data = {
            "name": "Test Project",
            "description": "This is a test project.",
            "github_link": "http://example.com/",
            "devpost_link": "http://example.com/",
        }
        self.project = Project(
            **self.project_data,
            team=self.team,
        )
        self.project.save()

        self.valoration_data = {
            "score":8,
        }
        self.valoration = Valoration(
            **self.valoration_data,
            project=self.project,
            admin=self.admin,
        )
        self.valoration.save()

        self.base_url = f'/event/{self.event.id}/project/'

    def test_project_view_get(self):
        """
        Test the project view GET request.
        """
        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/project/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 302)

        self.project.delete()
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects.html')

    def test_project_create_view_get(self):
        """
        Test the project create view GET request.
        """
        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/project/create/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 302)

        self.project.delete()
        response = self.client.get(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectCreate.html')

        self.team.delete()
        response = self.client.get(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 302)

    def test_project_create_view_post(self):
        """
        Test the project create view POST request.
        """
        response = self.client.post(f'/event/00000000-0000-0000-0000-000000000000/project/create/', {})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}create/', {})
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f'{self.base_url}create/', {})
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.post(f'{self.base_url}create/', {})
        self.assertEqual(response.status_code, 302)


        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post(f'{self.base_url}create/', {})
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'projectCreate.html')

        form_data = {
            'name': 'New Project',
            'description': 'This is a new project.',
            'github_link': 'http://new-example.com/',
            'devpost_link': 'http://new-example.com/',
        }
        
        response = self.client.post(f'{self.base_url}create/', form_data)
        self.assertEqual(response.status_code, 302)

        self.team.delete()
        response = self.client.post(f'{self.base_url}create/', {})
        self.assertEqual(response.status_code, 403)

    def test_project_CRUD_view_get(self):
        """
        Test the project CRUD view GET request.
        """
        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/project/{self.project.id}/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'/event/{self.event.id}/project/00000000-0000-0000-0000-000000000000/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}{self.project.id}/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f'{self.base_url}{self.project.id}/')
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(f'{self.base_url}{self.project.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectDetail.html')

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f'{self.base_url}{self.project.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectEdit.html')

        team2 = Team(
            name="Another Team",
            event=self.event2,
        )
        team2.save()
        self.project.team = team2
        self.project.save()
        response = self.client.get(f'{self.base_url}{self.project.id}/')
        self.assertEqual(response.status_code, 403)

        self.team.delete()
        response = self.client.get(f'{self.base_url}{self.project.id}/')
        self.assertEqual(response.status_code, 302)

    def test_project_CRUD_view_post(self):
        """
        Test the project CRUD view POST request.
        """
        response = self.client.post(f'/event/00000000-0000-0000-0000-000000000000/project/{self.project.id}/', {})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'/event/{self.event.id}/project/00000000-0000-0000-0000-000000000000/', {})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}{self.project.id}/', {})
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f'{self.base_url}{self.project.id}/', {})
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.post(f'{self.base_url}{self.project.id}/', {})
        self.assertEqual(response.status_code, 302)

        form_data = {
            'name': 'Updated Project',
            'description': 'This is an updated project.',
            'github_link': 'http://updated-example.com/',
            'devpost_link': 'http://updated-example.com/',
        }
        
        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post(f'{self.base_url}{self.project.id}/', form_data)
        self.assertEqual(response.status_code, 200)

        updated_project = ProjectService.get_project(self.project.id)
        self.assertEqual(updated_project.name, form_data['name'])
        self.assertEqual(updated_project.description, form_data['description'])
        self.assertEqual(updated_project.github_link, form_data['github_link'])
        self.assertEqual(updated_project.devpost_link, form_data['devpost_link'])

        team2 = Team(
            name="Another Team",
            event=self.event2,
        )
        team2.save()
        self.project.team = team2
        self.project.save()
        
        response = self.client.post(f'{self.base_url}{self.project.id}/', form_data)
        self.assertEqual(response.status_code, 403)

        self.team.delete()
        response = self.client.post(f'{self.base_url}{self.project.id}/', form_data)
        self.assertEqual(response.status_code, 302)

    def test_project_CRUD_view_delte(self):
        """
        Test the project CRUD view DELETE request.
        """
        response = self.client.delete(f'/event/00000000-0000-0000-0000-000000000000/project/{self.project.id}/', {})
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f'/event/{self.event.id}/project/00000000-0000-0000-0000-000000000000/', {})
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f'{self.base_url}{self.project.id}/', {})
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.delete(f'{self.base_url}{self.project.id}/', {})
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.delete(f'{self.base_url}{self.project.id}/', {})
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.delete(f'{self.base_url}{self.project.id}/', {})
        self.assertEqual(response.status_code, 204)

        with self.assertRaises(ValueError):
            ProjectService.get_project(self.project.id)

        team2 = Team(
            name="Another Team",
            event=self.event2,
        )
        team2.save()
        self.project.team = team2
        self.project.save()
        
        response = self.client.delete(f'{self.base_url}{self.project.id}/', {})
        self.assertEqual(response.status_code, 403)

        self.team.delete()
        response = self.client.delete(f'{self.base_url}{self.project.id}/', {})
        self.assertEqual(response.status_code, 302)

    def test_valoration_view_get(self):
        """
        Test the valoration view GET request.
        """
        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/project/{self.project.id}/valorate/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'/event/{self.event.id}/project/00000000-0000-0000-0000-000000000000/valorate/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}{self.project.id}/valorate/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f'{self.base_url}{self.project.id}/valorate/')
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(f'{self.base_url}{self.project.id}/valorate/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectValoration.html')

    def test_valoration_view_post(self):
        """
        Test the valoration view POST request.
        """
        response = self.client.post(f'/event/00000000-0000-0000-0000-000000000000/project/{self.project.id}/valorate/', {})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'/event/{self.event.id}/project/00000000-0000-0000-0000-000000000000/valorate', {})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}{self.project.id}/valorate/', {})
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f'{self.base_url}{self.project.id}/valorate/', {})
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.post(f'{self.base_url}{self.project.id}/valorate/', {})
        self.assertEqual(response.status_code, 400)

        form_data = {
            'score': 9,
        }
        
        response = self.client.post(f'{self.base_url}{self.project.id}/valorate/', form_data)
        self.assertEqual(response.status_code, 302)
