import uuid
from django.test import TestCase

from Apps.activity.forms import ActivityForm
from Apps.activity.models import Activity
from Apps.activity.services import ActivityService
from Apps.event.models import Event
from Apps.participant.models import Admin, Hacker, Mentor, Sponsor, Volunteer
from Apps.users.models import CustomUser


class ModelActivityTestCase(TestCase):
    """
    Test case for the Activity model.
    """

    def setUp(self):
        """
        Set up the test case.
        """
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
            "accepted_date": None,
            "application_date": "2000-01-01",
            "phone_number": "+1234567890",
            "type": "Hacker",
            "accepted_terms_and_conditions": True,
            "t_shirt_size": "M",
            "origin": "Spain",
            "status": "Under Review",
            "university": "Test University",
            "degree": "Computer Science",
            "graduation_year": 2024,
            "under_age": False,
            "lenny_face": "( ͡° ͜ʖ ͡°)",
            "hear_about_us": "From a friend",
            "why_excited": "I love coding and innovation!",
            "first_hackathon": True,
            "personal_projects": "My personal projects include a weather app and a portfolio website.",
            "share_cv": True,
            "subscribe": True,
        }

        self.hacker = Hacker(
            **self.hacker_data,
            event=self.event,
            user=self.user1,
        )
        self.hacker.save()

    def test_activity_creation(self):
        """
        Test the creation of an activity.
        """
        activity = Activity(
            name="Test Activity",
            type="MEAL",
            description="This is a test activity.",
            start_date="2023-10-01T10:00:00Z",
            end_date="2023-10-01T11:00:00Z",
            event=self.event,
        )
        activity.full_clean()
        activity.save()
        self.assertIsInstance(activity, Activity)
        self.assertEqual(activity.name, "Test Activity")
        self.assertEqual(activity.type, "MEAL")
        self.assertEqual(activity.description, "This is a test activity.")
        self.assertEqual(str(activity.start_date), "2023-10-01 10:00:00+00:00")
        self.assertEqual(str(activity.end_date), "2023-10-01 11:00:00+00:00")
        self.assertEqual(activity.event, self.event)

    def test_activity_incorrect_data_creation(self):
        """
        Test the creation of an activity with incorrect data.
        """
        activity = Activity(
            name="Test Activity",
            type="MEAL",
            description="This is a test activity.",
            start_date="2023-10-01T12:00:00Z",
            end_date="2023-10-01T11:00:00Z",  # End date before start date
            event=self.event,
        )
        with self.assertRaises(Exception):
            activity.full_clean()
            activity.save()


class ServiceActivityTestCase(TestCase):
    """
    Test case for the Activity service.
    """

    def setUp(self):
        """
        Set up the test case.
        """
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
            "accepted_date": None,
            "application_date": "2000-01-01",
            "phone_number": "+1234567890",
            "type": "Hacker",
            "accepted_terms_and_conditions": True,
            "t_shirt_size": "M",
            "origin": "Spain",
            "status": "Under Review",
            "university": "Test University",
            "degree": "Computer Science",
            "graduation_year": 2024,
            "under_age": False,
            "lenny_face": "( ͡° ͜ʖ ͡°)",
            "hear_about_us": "From a friend",
            "why_excited": "I love coding and innovation!",
            "first_hackathon": True,
            "personal_projects": "My personal projects include a weather app and a portfolio website.",
            "share_cv": True,
            "subscribe": True,
        }

        self.hacker = Hacker(
            **self.hacker_data,
            event=self.event,
            user=self.user1,
        )
        self.hacker.save()

        self.mentor_data = {
            "application_date": "2000-01-01",
            "phone_number": "+1234567890",
            "type": "Mentor",
            "accepted_terms_and_conditions": True,
            "t_shirt_size": "M",
            "origin": "Spain",
            "status": "Under Review",
            "university": "Test University",
            "degree": "Computer Science",
            "position": "Software Engineer",
            "english_level": "Low",
            "hear_about_us": "From a friend",
            "personal_projects": "I have worked on several open-source projects.",
            "first_hackathon": True,
            "subscribe": True,
        }

        self.sponsor_data = {
            "application_date": "2000-01-01",
            "phone_number": "+1234567890",
            "type": "Sponsor",
            "accepted_terms_and_conditions": True,
            "t_shirt_size": "M",
            "origin": "Spain",
            "status": "Under Review",
            "company_name": "Test Company",
            "position": "A leading tech company.",
        }

        self.volunteer_data = {
            "application_date": "2000-01-01",
            "phone_number": "+1234567890",
            "type": "Volunteer",
            "accepted_terms_and_conditions": True,
            "t_shirt_size": "M",
            "origin": "Spain",
            "status": "Under Review",
            "university": "Test University",
            "degree": "Computer Science",
            "position": "Event Volunteer",
            "languages": "English, Spanish",
            "first_volunteering": True,
            "hear_about_us": "From a friend",
            "cool_skill": "I can juggle and do magic tricks.",
            "personal_qualities": "I am very organized and love helping others.",
            "personal_weakness": "I can be a bit shy at first, but I warm up quickly.",
            "motivation": "I want to contribute to the success of the event and meet new people.",
            "nigth_shifts": True,
            "subscribe": True,
        }

        self.admin_data = {
            "application_date": "2000-01-01",
            "phone_number": "+1234567890",
            "type": "Admin",
            "accepted_terms_and_conditions": True,
            "t_shirt_size": "M",
            "origin": "Spain",
            "status": "Under Review",
        }
        self.admin = Admin(**self.admin_data, user=self.user1, event=self.event)
        self.admin.save()
        self.mentor = Mentor(
            **self.mentor_data,
            user=self.user1,
            event=self.event,
        )
        self.mentor.save()
        self.sponsor = Sponsor(
            **self.sponsor_data,
            user=self.user1,
            event=self.event,
        )
        self.sponsor.save()
        self.volunteer = Volunteer(
            **self.volunteer_data,
            user=self.user1,
            event=self.event,
        )
        self.volunteer.save()

    def test_get_activity(self):
        """
        Test the retrieval of an activity.
        """
        activity = Activity(
            name="Test Activity",
            type="MEAL",
            description="This is a test activity.",
            start_date="2023-10-01T10:00:00Z",
            end_date="2023-10-01T11:00:00Z",
            event=self.event,
        )
        activity.save()

        retrieved_activity = ActivityService.get_activity(activity.id)
        self.assertIsNotNone(retrieved_activity)
        self.assertEqual(retrieved_activity, activity)

        non_existent_activity = ActivityService.get_activity(uuid.uuid4())
        self.assertIsNone(non_existent_activity)

    def test_get_all_activities(self):
        """
        Test the retrieval of all activities for an event.
        """
        activity1 = Activity(
            name="Test Activity 1",
            type="MEAL",
            description="This is a test activity 1.",
            start_date="2023-10-01T10:00:00Z",
            end_date="2023-10-01T11:00:00Z",
            event=self.event,
        )
        activity1.save()

        activity2 = Activity(
            name="Test Activity 2",
            type="WORKSHOP",
            description="This is a test activity 2.",
            start_date="2023-10-01T12:00:00Z",
            end_date="2023-10-01T13:00:00Z",
            event=self.event,
        )
        activity2.save()

        activities = ActivityService.get_all_activities(self.event)
        self.assertIn(activity1, activities)
        self.assertIn(activity2, activities)
        self.assertEqual(len(activities), 2)

    def test_filter_by_name_or_id(self):
        """
        Test filtering activities by name or ID.
        """
        activity1 = Activity(
            name="Test Activity 1",
            type="MEAL",
            description="This is a test activity 1.",
            start_date="2023-10-01T10:00:00Z",
            end_date="2023-10-01T11:00:00Z",
            event=self.event,
        )
        activity1.save()

        activity2 = Activity(
            name="Test Activity 2",
            type="WORKSHOP",
            description="This is a test activity 2.",
            start_date="2023-10-01T12:00:00Z",
            end_date="2023-10-01T13:00:00Z",
            event=self.event,
        )
        activity2.save()

        activities = ActivityService.get_all_activities(self.event)

        filtered_activities = ActivityService.filter_by_name_or_id(
            activities, "Test Activity 1"
        )
        self.assertIn(activity1, filtered_activities)
        self.assertNotIn(activity2, filtered_activities)

        filtered_activities = ActivityService.filter_by_name_or_id(
            activities, str(activity2.id)
        )
        self.assertIn(activity2, filtered_activities)
        self.assertNotIn(activity1, filtered_activities)

        non_existent_filtered = ActivityService.filter_by_name_or_id(
            activities, "Non Existent Activity"
        )
        self.assertEqual(len(non_existent_filtered), 0)

    def test_filter_by_type(self):
        """
        Test filtering activities by type.
        """
        activity1 = Activity(
            name="Test Activity 1",
            type="MEAL",
            description="This is a test activity 1.",
            start_date="2023-10-01T10:00:00Z",
            end_date="2023-10-01T11:00:00Z",
            event=self.event,
        )
        activity1.save()

        activity2 = Activity(
            name="Test Activity 2",
            type="WORKSHOP",
            description="This is a test activity 2.",
            start_date="2023-10-01T12:00:00Z",
            end_date="2023-10-01T13:00:00Z",
            event=self.event,
        )
        activity2.save()

        activities = ActivityService.get_all_activities(self.event)

        filtered_activities = ActivityService.filter_by_type(activities, "MEAL")
        self.assertIn(activity1, filtered_activities)
        self.assertNotIn(activity2, filtered_activities)

        filtered_activities = ActivityService.filter_by_type(activities, "WORKSHOP")
        self.assertIn(activity2, filtered_activities)
        self.assertNotIn(activity1, filtered_activities)

        filtered_activities = ActivityService.filter_by_type(
            activities, "NON_EXISTENT_TYPE"
        )
        self.assertEqual(len(filtered_activities), 0)

    def test_create_activity(self):
        """
        Test the creation of an activity using the service.
        """
        activity_data = {
            "name": "Service Test Activity",
            "type": "MEAL",
            "description": "This is a service test activity.",
            "start_date": "2023-10-01T10:00:00Z",
            "end_date": "2023-10-01T11:00:00Z",
        }
        form = ActivityForm(data=activity_data)
        self.assertTrue(form.is_valid())
        activity = ActivityService.create_activity(form, self.event)
        self.assertIsInstance(activity, Activity)
        self.assertEqual(activity.name, "Service Test Activity")
        self.assertEqual(activity.type, "MEAL")
        self.assertEqual(activity.description, "This is a service test activity.")
        self.assertEqual(str(activity.start_date), "2023-10-01 10:00:00+00:00")
        self.assertEqual(str(activity.end_date), "2023-10-01 11:00:00+00:00")
        self.assertEqual(activity.event, self.event)

    def test_update_activity(self):
        """
        Test the update of an activity using the service.
        """
        activity = Activity(
            name="Test Activity",
            type="MEAL",
            description="This is a test activity.",
            start_date="2023-10-01T10:00:00Z",
            end_date="2023-10-01T11:00:00Z",
            event=self.event,
        )
        activity.save()

        updated_data = {
            "name": "Updated Test Activity",
            "type": "WORKSHOP",
            "description": "This is an updated test activity.",
            "start_date": "2023-10-01T12:00:00Z",
            "end_date": "2023-10-01T13:00:00Z",
        }

        form = ActivityForm(instance=activity, data=updated_data)
        self.assertTrue(form.is_valid())

        updated_activity = ActivityService.update_activity(activity, form.cleaned_data)

        self.assertEqual(updated_activity.name, "Updated Test Activity")
        self.assertEqual(updated_activity.type, "WORKSHOP")
        self.assertEqual(
            updated_activity.description, "This is an updated test activity."
        )
        self.assertEqual(str(updated_activity.start_date), "2023-10-01 12:00:00+00:00")
        self.assertEqual(str(updated_activity.end_date), "2023-10-01 13:00:00+00:00")

    def test_delete_activity(self):
        """
        Test the deletion of an activity using the service.
        """
        activity = Activity(
            name="Test Activity",
            type="MEAL",
            description="This is a test activity.",
            start_date="2023-10-01T10:00:00Z",
            end_date="2023-10-01T11:00:00Z",
            event=self.event,
        )
        activity.save()

        self.assertTrue(ActivityService.delete_activity(activity))
        self.assertEqual(Activity.objects.count(), 0)

    def test_checkin_participant(self):
        """
        Test checking in a participant to an activity.
        """
        activity = Activity(
            name="Test Activity",
            type="MEAL",
            description="This is a test activity.",
            start_date="2023-10-01T10:00:00Z",
            end_date="2023-10-01T11:00:00Z",
            event=self.event,
        )
        activity.save()

        ActivityService.checkin_participant(activity, self.hacker)
        self.assertIn(self.hacker, activity.hacker_participants.all())

        ActivityService.checkin_participant(activity, self.mentor)
        self.assertIn(self.mentor, activity.mentor_participants.all())

        ActivityService.checkin_participant(activity, self.sponsor)
        self.assertIn(self.sponsor, activity.sponsor_participants.all())

        ActivityService.checkin_participant(activity, self.volunteer)
        self.assertIn(self.volunteer, activity.volunteer_participants.all())

        ActivityService.checkin_participant(activity, self.admin)
        self.assertIn(self.admin, activity.admin_participants.all())

    def test_get_participant_count(self):
        """
        Test getting the participant count for an activity.
        """
        activity = Activity(
            name="Test Activity",
            type="MEAL",
            description="This is a test activity.",
            start_date="2023-10-01T10:00:00Z",
            end_date="2023-10-01T11:00:00Z",
            event=self.event,
        )
        activity.save()

        ActivityService.checkin_participant(activity, self.hacker)
        ActivityService.checkin_participant(activity, self.mentor)

        count = ActivityService.get_participant_count(activity)
        self.assertEqual(count, 2)


class ViewActivityTestCase(TestCase):
    """
    Test case for the Activity views.
    """

    def setUp(self):
        """
        Set up the test case.
        """
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
            "accepted_date": None,
            "application_date": "2000-01-01",
            "phone_number": "+1234567890",
            "type": "Hacker",
            "accepted_terms_and_conditions": True,
            "t_shirt_size": "M",
            "origin": "Spain",
            "status": "Under Review",
            "university": "Test University",
            "degree": "Computer Science",
            "graduation_year": 2024,
            "under_age": False,
            "lenny_face": "( ͡° ͜ʖ ͡°)",
            "hear_about_us": "From a friend",
            "why_excited": "I love coding and innovation!",
            "first_hackathon": True,
            "personal_projects": "My personal projects include a weather app and a portfolio website.",
            "share_cv": True,
            "subscribe": True,
        }

        self.hacker = Hacker(
            **self.hacker_data,
            event=self.event,
            user=self.user1,
        )
        self.hacker.save()

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

        self.activity_data = {
            "name": "New Activity",
            "type": "MEAL",
            "description": "This is a new activity.",
            "start_date": "2023-10-01T10:00:00Z",
            "end_date": "2023-10-01T11:00:00Z",
        }
        self.base_url = f"/event/{self.event.id}/activity/"

    def test_activity_view_get(self):
        """
        Test the activity view GET method.
        """
        response = self.client.get(
            f"/event/00000000-0000-0000-0000-000000000000/activity/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.base_url}")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f"{self.base_url}")
        self.assertEqual(response.status_code, 302)

        self.admin.save()
        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f"{self.base_url}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activities.html")

        response = self.client.get(f"{self.base_url}?search=Test&type=MEAL")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activities.html")

    def test_activity_create_view_get(self):
        """
        Test the activity create view GET method.
        """
        response = self.client.get(
            f"/event/00000000-0000-0000-0000-000000000000/activity/create/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.base_url}create/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f"{self.base_url}create/")
        self.assertEqual(response.status_code, 302)

        self.admin.save()
        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f"{self.base_url}create/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activityCreate.html")

    def test_activity_create_view_post(self):
        """
        Test the activity create view POST method.
        """
        response = self.client.post(
            f"/event/00000000-0000-0000-0000-000000000000/activity/create/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f"{self.base_url}create/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post(f"{self.base_url}create/")
        self.assertEqual(response.status_code, 302)

        self.admin.save()
        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(
            f"{self.base_url}create/",
            data=self.activity_data,
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            f"{self.base_url}create/",
            data={
                "name": "",
                "type": "MEAL",
                "description": "This is a new activity.",
                "start_date": "2024-10-01T10:00:00Z",
                "end_date": "2023-10-01T11:00:00Z",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_activity_CRUD_view_get(self):
        """
        Test the activity CRUD view GET method.
        """
        response = self.client.get(
            f"/event/00000000-0000-0000-0000-000000000000/activity/00000000-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(
            f"{self.base_url}00000000-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(
            f"{self.base_url}00000000-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 302)

        self.admin.save()
        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(
            f"{self.base_url}00000000-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 302)

        activity = Activity(**self.activity_data, event=self.event)
        activity.save()
        response = self.client.get(f"{self.base_url}{activity.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activityEdit.html")

    def test_activity_CRUD_view_post(self):
        """
        Test the activity CRUD view POST method.
        """
        response = self.client.post(
            f"/event/00000000-0000-0000-0000-000000000000/activity/00000000-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            f"{self.base_url}00000000-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 302)

        activity = Activity(**self.activity_data, event=self.event)
        activity.save()

        response = self.client.post(f"{self.base_url}{activity.id}/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post(f"{self.base_url}{activity.id}/")
        self.assertEqual(response.status_code, 302)

        self.admin.save()
        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(
            f"{self.base_url}{activity.id}/",
            data=self.activity_data,
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            f"{self.base_url}{activity.id}/",
            data={
                "name": "Updated Activity",
                "type": "WORKSHOP",
                "description": "This is an updated activity.",
                "start_date": "2024-10-01T12:00:00Z",
                "end_date": "2023-10-01T13:00:00Z",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_activity_CRUD_view_delete(self):
        """
        Test the activity CRUD view DELETE method.
        """
        response = self.client.delete(
            f"/event/00000000-0000-0000-0000-000000000000/activity/00000000-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(
            f"{self.base_url}00000000-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 302)

        activity = Activity(**self.activity_data, event=self.event)
        activity.save()

        response = self.client.delete(f"{self.base_url}{activity.id}/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.delete(f"{self.base_url}{activity.id}/")
        self.assertEqual(response.status_code, 302)
    
        self.admin.save()
        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.delete(f"{self.base_url}{activity.id}/")
        self.assertEqual(response.status_code, 204)

    def test_activity_checkin_view(self):
        """
        Test the activity check-in view.
        """
        response = self.client.get(
            f"/event/00000000-0000-0000-0000-000000000000/activity/00000000-0000-0000-0000-000000000000/checkin/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.base_url}00000000-0000-0000-0000-000000000000/checkin/")
        self.assertEqual(response.status_code, 302)

        activity = Activity(**self.activity_data, event=self.event)
        activity.save()

        response = self.client.get(f"{self.base_url}{activity.id}/checkin/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f"{self.base_url}{activity.id}/checkin/")
        self.assertEqual(response.status_code, 302)

        self.admin.save()
        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f"{self.base_url}{activity.id}/checkin/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activityCheckIn.html")
    
    def test_activity_checkin_view_post(self):
        """
        Test the activity check-in view POST method.
        """
        response = self.client.post(
            f"/event/00000000-0000-0000-0000-000000000000/activity/00000000-0000-0000-0000-000000000000/checkin/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f"{self.base_url}00000000-0000-0000-0000-000000000000/checkin/")
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f"{self.base_url}00000000-0000-0000-0000-000000000000/checkin/", {"qrResult": "00000000-0000-0000-0000-000000000000"}, content_type="application/json")
        self.assertEqual(response.status_code, 404)

        activity = Activity(**self.activity_data, event=self.event)
        activity.save()

        response = self.client.post(f"{self.base_url}{activity.id}/checkin/", {"qrResult": "00000000-0000-0000-0000-000000000000"}, content_type="application/json")
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f"{self.base_url}{activity.id}/checkin/",  {"qrResult": f"{self.hacker.id}"}, content_type="application/json")
        self.assertEqual(response.status_code, 401)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post(f"{self.base_url}{activity.id}/checkin/",  {"qrResult": f"{self.hacker.id}"}, content_type="application/json")
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f"{self.base_url}{activity.id}/checkin/", {"qrResult": f"{self.hacker.id}"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        response = self.client.post(f"{self.base_url}{activity.id}/checkin/", {"qrResult": f"{self.hacker.id}"}, content_type="application/json")
        self.assertEqual(response.status_code, 409)
