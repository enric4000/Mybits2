from django.test import TestCase

from Apps.event.models import Event
from Apps.participant.models import Admin, Hacker
from Apps.team.forms import TeamForm
from Apps.team.models import Team
from Apps.team.services import TeamService
from Apps.users.models import CustomUser


# Create your tests here.
class ModelTeamTestCase(TestCase):
    """
    Test case for the Team model.
    """

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

        self.team_data = {
            "name": "Test Team",
        }

    def test_team_creation(self):
        """
        Test the creation of a team
        """
        team = Team(**self.team_data, event=self.event)
        team.members.add(self.hacker)
        team.clean()
        team.save()
        self.assertEqual(team.name, "Test Team")
        self.assertEqual(team.members.count(), 1)
        self.assertEqual(team.members.first(), self.hacker)
        self.assertEqual(team.event, self.event)
        self.assertTrue(team.id)

    def test_team_creation_incorrect_data(self):
        """
        Test the creation of a team with incorrect data
        """
        team = Team(event=self.event)
        team.members.add(self.hacker)

        hacker2 = Hacker(
            **self.hacker_data,
            event=self.event,
            user=self.user1,
        )

        hacker3 = Hacker(
            **self.hacker_data,
            event=self.event,
            user=self.user1,
        )

        hacker4 = Hacker(
            **self.hacker_data,
            event=self.event,
            user=self.user1,
        )

        hacker5 = Hacker(
            **self.hacker_data,
            event=self.event,
            user=self.user1,
        )
        hacker2.save()
        hacker3.save()
        hacker4.save()
        hacker5.save()
        team = Team(
            name="Test Team with Too Many Members",
            event=self.event,
        )
        team.save()
        team.members.add(self.hacker)
        team.members.add(hacker2)
        team.members.add(hacker3)
        team.members.add(hacker4)
        team.members.add(hacker5)

        with self.assertRaises(Exception):
            team.clean()
            team.save()
    
    def tearDown(self):
        for team in Team.objects.all():
            team.delete()

        for participant in Hacker.objects.all():
            participant.delete()

        for user in CustomUser.objects.all():
            user.delete()

        for event in Event.objects.all():
            event.delete()

        return super().tearDown()

class ServiceTeamTestCase(TestCase):
    """
    Test case for the Team service.
    """

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

        self.team_data = {
            "name": "Test Team"
        }

    def test_team_service_creation(self):
        """
        Test the creation of a team using the TeamService.
        """
        form = TeamForm(self.team_data)
        TeamService.create_team(form, self.event, self.hacker)
        self.assertTrue(Team.objects.filter(name="Test Team").exists())
        form = TeamForm()

        with self.assertRaises(Exception):
            TeamService.create_team(form, self.hacker, self.event)

    def test_team_service_get_by_event_and_participant(self):
        """
        Test the retrieval of a team by event and participant.
        """
        form = TeamForm(self.team_data)
        team = TeamService.create_team(form, self.event, self.hacker)

        team = TeamService.get_team_by_event_and_participant(
            self.event, self.hacker
        )
        self.assertIsNotNone(team)
        self.assertEqual(team.name, "Test Team")
        self.assertEqual(team.members.count(), 1)
        self.assertEqual(team.members.first(), self.hacker)
        self.assertEqual(team.event, self.event)

        team = TeamService.get_team_by_event_and_participant(
            self.event, None
        )
        self.assertIsNone(team)

        team = TeamService.get_team_by_event_and_participant(
            None, self.hacker
        )
        self.assertIsNone(team)


    def test_team_service_get_all_teams(self):
        """
        Test the retrieval of all teams for an event.
        """
        form = TeamForm(self.team_data)
        team = TeamService.create_team(form, self.event, self.hacker)

        teams = TeamService.get_all_teams(self.event)
        self.assertEqual(teams.count(), 1)
        self.assertEqual(teams.first(), team)

    def test_team_service_filter_by_name_or_id(self):
        """
        Test the filtering of teams by name or ID.
        """
        form = TeamForm(self.team_data)
        team = TeamService.create_team(form, self.event, self.hacker)

        teams = TeamService.filter_by_name_or_id(self.event, "Test Team", Team.objects.all())
        self.assertEqual(teams.count(), 1)
        self.assertEqual(teams.first(), team)

        teams = TeamService.filter_by_name_or_id(self.event, team.id, Team.objects.all())
        self.assertEqual(teams.count(), 1)
        self.assertEqual(teams.first(), team)

        teams = TeamService.filter_by_name_or_id(self.event, "Nonexistent", Team.objects.all())
        self.assertEqual(teams.count(), 0)

    def test_team_service_get_team(self):
        """
        Test the retrieval of a team by ID.
        """
        form = TeamForm(self.team_data)
        team = TeamService.create_team(form, self.event, self.hacker)

        retrieved_team = TeamService.get_team(team.id)
        self.assertEqual(retrieved_team, team)

        retrieved_team = TeamService.get_team("00000000-0000-0000-0000-000000000000")
        self.assertIsNone(retrieved_team)

    def test_team_service_update_team(self):
        """
        Test the update of a team using the TeamService.
        """
        form = TeamForm(self.team_data)
        team = TeamService.create_team(form, self.event, self.hacker)

        updated_data = {
            "name": "Updated Test Team"
        }
        updated_team = TeamService.update_team(team, updated_data)
        self.assertEqual(updated_team.name, "Updated Test Team")

        result = TeamService.update_team(None, updated_data)
        self.assertIsNone(result)

    def test_team_service_add_member(self):
        """
        Test the addition of a member to a team using the TeamService.
        """
        form = TeamForm(self.team_data)
        team = TeamService.create_team(form, self.event, self.hacker)

        new_hacker_data = {
            "accepted_date":None,
            "application_date":"2000-01-01",
            "phone_number":"+1234567891",
            "type":"Hacker",
            "accepted_terms_and_conditions":True,
            "t_shirt_size":"M",
            "origin":"Spain",
            "status":"Under Review",
            "university":"Test University 2",
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

        new_hacker = Hacker(
            **new_hacker_data,
            event=self.event,
            user=self.user1,
        )
        new_hacker.save()

        updated_team = TeamService.add_member(team, new_hacker)
        self.assertEqual(updated_team.members.count(), 2)
        self.assertIn(new_hacker, updated_team.members.all())

        with self.assertRaises(Exception):
            TeamService.add_member(team, None)

    def test_team_service_delete_member(self):
        """
        Test the deletion of a member from a team using the TeamService.
        """
        form = TeamForm(self.team_data)
        team = TeamService.create_team(form, self.event, self.hacker)

        new_hacker_data = {
            "accepted_date":None,
            "application_date":"2000-01-01",
            "phone_number":"+1234567891",
            "type":"Hacker",
            "accepted_terms_and_conditions":True,
            "t_shirt_size":"M",
            "origin":"Spain",
            "status":"Under Review",
            "university":"Test University 2",
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

        new_hacker = Hacker(
            **new_hacker_data,
            event=self.event,
            user=self.user1,
        )
        new_hacker.save()

        updated_team = TeamService.add_member(team, new_hacker)
        updated_team = TeamService.delete_member(updated_team, new_hacker)
        self.assertEqual(updated_team.members.count(), 1)
        self.assertNotIn(new_hacker, updated_team.members.all())

        result = TeamService.delete_member(updated_team, None)
        self.assertIsNone(result)
        self.assertEqual(Team.objects.count(), 1)

        team = TeamService.delete_member(updated_team, self.hacker)
        self.assertEqual(team.members.count(), 0)

    def test_team_service_get_team_participants(self):
        """
        Test the retrieval of team participants using the TeamService.
        """
        form = TeamForm(self.team_data)
        team = TeamService.create_team(form, self.event, self.hacker)


        participants = TeamService.get_team_participants(team)
        self.assertEqual(len(participants), 1)
        self.assertIn(self.user1.first_name, str(participants[0].values()))

    def test_team_service_delete_team(self):
        """
        Test the deletion of a team using the TeamService.
        """
        form = TeamForm(self.team_data)
        team = TeamService.create_team(form, self.event, self.hacker)

        deleted = TeamService.delete_team(team)
        self.assertTrue(deleted)
        self.assertEqual(Team.objects.count(), 0)

        deleted = TeamService.delete_team(None)
        self.assertFalse(deleted)

    def test_team_service_to_dict(self):
        """
        Test the conversion of a team to a dictionary using the TeamService.
        """
        form = TeamForm(self.team_data)
        team = TeamService.create_team(form, self.event, self.hacker)

        team_dict = TeamService.team_to_dict(team)
        self.assertIn("Test Team", str(team_dict[0].values()))

class ViewTeamTestCase(TestCase):
    """
    Test case for the Team views.
    """

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

        self.user1 = CustomUser.objects.create(
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

        self.team_data = {
            "name":"Test Team"
        }
        self.base_url = f"/event/{self.event.id}/team/"

    def test_team_view_get(self):
        response = self.client.get("/event/00000000-0000-0000-0000-000000000000/team/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 302)
        
        Admin(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user2,
        ).save()

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "teams.html")

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 302)

        team = Team(**self.team_data, event=self.event)
        team.members.add(self.hacker)
        team.save()
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 302)
    

    def test_team_create_view_get(self):
        response = self.client.get("/event/00000000-0000-0000-0000-000000000000/team/create/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.base_url}create/")
        self.assertEqual(response.status_code, 302)

        Admin(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user2,
        ).save()

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f"{self.base_url}create/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f"{self.base_url}create/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "teamCreate.html")

        team = Team(**self.team_data, event=self.event)
        team.members.add(self.hacker)
        team.save()
        response = self.client.get(f"{self.base_url}create/")
        self.assertEqual(response.status_code, 302)

    def test_team_create_view_post(self):
        response = self.client.post("/event/00000000-0000-0000-0000-000000000000/team/create/")
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f"{self.base_url}create/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f"{self.base_url}create/")
        self.assertEqual(response.status_code, 302)

        Admin(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user2,
        ).save()

        response = self.client.post(f"{self.base_url}create/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post(f"{self.base_url}create/")
        self.assertEqual(response.status_code, 400)

        response = self.client.post(f"{self.base_url}create/", self.team_data)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(f"{self.base_url}create/", self.team_data)
        self.assertEqual(response.status_code, 302)

    def test_team_CRUD_view_get(self):
        response = self.client.get("/event/00000000-0000-0000-0000-000000000000/team/00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.base_url}00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f"{self.base_url}00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 302)

        Admin(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user2,
        ).save()

        response = self.client.get(f"{self.base_url}00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 404)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f"{self.base_url}00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 404)

        team = Team(**self.team_data, event=self.event)
        team.members.add(self.hacker)
        team.save()
        response = self.client.get(f"{self.base_url}{team.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "teamEdit.html")

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f"{self.base_url}{team.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "teamDetail.html")

    def test_team_CRUD_view_post(self):
        response = self.client.post("/event/00000000-0000-0000-0000-000000000000/team/00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f"{self.base_url}00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f"{self.base_url}00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 302)

        Admin(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user2,
        ).save()

        response = self.client.post(f"{self.base_url}00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post(f"{self.base_url}00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 302)

        team = Team(**self.team_data, event=self.event)
        team.members.add(self.hacker)
        team.save()
        response = self.client.post(f"{self.base_url}{team.id}/")
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "teamEdit.html")

        response = self.client.post(f"{self.base_url}{team.id}/", self.team_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "teamEdit.html")

    def test_team_CRUD_view_delete(self):
        response = self.client.delete("/event/00000000-0000-0000-0000-000000000000/team/00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f"{self.base_url}00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.delete(f"{self.base_url}00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 302)


        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.delete(f"{self.base_url}00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.delete(f"{self.base_url}00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 404)

        team = Team(**self.team_data, event=self.event)
        team.members.add(self.hacker)
        team.save()
        response = self.client.delete(f"{self.base_url}{team.id}/")
        self.assertEqual(response.status_code, 204)

    def test_team_join_view_get(self):
        response = self.client.get("/event/00000000-0000-0000-0000-000000000000/team/join/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"/event/{self.event.id}/team/join/")
        self.assertEqual(response.status_code, 302)

        Admin(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user2,
        ).save()

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f"/event/{self.event.id}/team/join/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f"/event/{self.event.id}/team/join/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "teamJoin.html")
    
        team = Team(**self.team_data, event=self.event)
        team.members.add(self.hacker)
        team.save()
        response = self.client.get(f"/event/{self.event.id}/team/join/")
        self.assertEqual(response.status_code, 302)

    def test_team_join_view_post(self):
        response = self.client.post("/event/00000000-0000-0000-0000-000000000000/team/join/")
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f"/event/{self.event.id}/team/join/")
        self.assertEqual(response.status_code, 400)

        response = self.client.post(f"/event/{self.event.id}/team/join/", {"qrResult":"00000000-0000-0000-0000-000000000000"})
        self.assertEqual(response.status_code, 400)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f"/event/{self.event.id}/team/join/", {"qrResult":"00000000-0000-0000-0000-000000000000"})
        self.assertEqual(response.status_code, 400)

        Admin(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user2,
        ).save()

        response = self.client.post(f"/event/{self.event.id}/team/join/", {"qrResult":"00000000-0000-0000-0000-000000000000"})
        self.assertEqual(response.status_code, 400)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post(f"/event/{self.event.id}/team/join/", {"qrResult":"00000000-0000-0000-0000-000000000000"})
        self.assertEqual(response.status_code, 400)

        team = Team(**self.team_data, event=self.event)
        team.save()

        response = self.client.post(
            f"/event/{self.event.id}/team/join/",
            {"qrResult": str(team.id)},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            f"/event/{self.event.id}/team/join/",
            {"qrResult": str(team.id)},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 409)

    def test_team_id_view_get(self):
        response = self.client.get("/event/00000000-0000-0000-0000-000000000000/team/id/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"/event/{self.event.id}/team/id/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f"/event/{self.event.id}/team/id/")
        self.assertEqual(response.status_code, 302)

        Admin(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user2,
        ).save()

        response = self.client.get(f"/event/{self.event.id}/team/id/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f"/event/{self.event.id}/team/id/")
        self.assertEqual(response.status_code, 302)

        team = Team(**self.team_data, event=self.event)
        team.members.add(self.hacker)
        team.save()
        response = self.client.get(f"/event/{self.event.id}/team/id/")
        self.assertEqual(response.status_code, 200)  
