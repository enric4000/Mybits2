from django.test import TestCase

from Apps.event.models import Event
from Apps.event.services import EventService
from Apps.event.forms import EventForm
from Apps.participant.models import Admin
from Apps.users.models import CustomUser


# Create your tests here.
class ModelEventTestCase(TestCase):
    """
    Test case for the Event model.
    """

    def setUp(self):
        self.event_data = {
            "name": "Test Event",
            "AppName": "TestApp",
            "description": "This is a test event.",
            "location": "Test Location",
            "timezone": "UTC",
            "start_date": "2023-10-01T09:00:00Z",
            "end_date": "2023-10-02T18:00:00Z",
            "hacker_deadline": "2023-09-25T23:59:59Z",
            "mentor_deadline": "2023-09-26T23:59:59Z",
            "volunteer_deadline": "2023-09-27T23:59:59Z",
            "sponsor_deadline": "2023-09-28T23:59:59Z",
            "terms_and_conditions_link": "https://example.com/terms",
        }

    def test_event_creation(self):
        event = Event(**self.event_data)
        event.clean()
        event.save()
        self.assertEqual(event.name, "Test Event")
        self.assertEqual(event.AppName, "TestApp")
        self.assertEqual(event.description, "This is a test event.")
        self.assertEqual(event.location, "Test Location")
        self.assertEqual(event.timezone, "UTC")
        self.assertEqual(str(event.start_date), "2023-10-01T09:00:00Z")
        self.assertEqual(str(event.end_date), "2023-10-02T18:00:00Z")
        self.assertEqual(str(event.hacker_deadline), "2023-09-25T23:59:59Z")
        self.assertEqual(str(event.mentor_deadline), "2023-09-26T23:59:59Z")
        self.assertEqual(str(event.volunteer_deadline), "2023-09-27T23:59:59Z")
        self.assertEqual(str(event.sponsor_deadline), "2023-09-28T23:59:59Z")
        self.assertEqual(event.terms_and_conditions_link, "https://example.com/terms")

    def test_event_creation_incorrect_dates(self):
        event_modified_data = self.event_data.copy()
        event_modified_data["end_date"] = "2020-10-02T18:00:00Z"
        event = Event(**event_modified_data)

        with self.assertRaises(Exception) as context:
            event.clean()

        self.assertIn("start_date", str(context.exception))
        self.assertIn("hacker_deadline", str(context.exception))
        self.assertIn("mentor_deadline", str(context.exception))
        self.assertIn("volunteer_deadline", str(context.exception))
        self.assertIn("sponsor_deadline", str(context.exception))

    def test_event_creation_with_missing_fields(self):
        event_modified_data = self.event_data.copy()
        event_modified_data["terms_and_conditions_link"] = None
        event = Event(**event_modified_data)

        with self.assertRaises(Exception) as context:
            event.clean()
            event.save()

        self.assertIn("terms_and_conditions_link", str(context.exception))


class ServiceEventTestCase(TestCase):
    """
    Test case for the Event Service.
    """

    def setUp(self):
        self.event_data = {
            "name": "Service Test Event",
            "AppName": "ServiceTestApp",
            "description": "This is a service test event.",
            "location": "Service Test Location",
            "timezone": "UTC",
            "start_date": "2023-10-01T09:00:00Z",
            "end_date": "2023-10-02T18:00:00Z",
            "hacker_deadline": "2023-09-25T23:59:59Z",
            "mentor_deadline": "2023-09-26T23:59:59Z",
            "volunteer_deadline": "2023-09-27T23:59:59Z",
            "sponsor_deadline": "2023-09-28T23:59:59Z",
            "terms_and_conditions_link": "https://example.com/terms",
        }

        self.event_data2 = {
            "name": "Service Test Event 2",
            "AppName": "ServiceTestApp2",
            "description": "This is another service test event.",
            "location": "Service Test Location 2",
            "timezone": "UTC",
            "start_date": "2023-10-03T09:00:00Z",
            "end_date": "2023-10-04T18:00:00Z",
            "hacker_deadline": "2023-09-29T23:59:59Z",
            "mentor_deadline": "2023-09-30T23:59:59Z",
            "volunteer_deadline": "2023-10-01T23:59:59Z",
            "sponsor_deadline": "2023-10-02T23:59:59Z",
            "terms_and_conditions_link": "https://example.com/terms2",
        }

        self.event = Event.objects.create(**self.event_data)

    def test_event_service_creation(self):
        form = EventForm(self.event_data2)
        EventService.create_event(form)
        self.assertEqual(Event.objects.count(), 2)
        self.assertIsNotNone(Event.objects.filter(name="Service Test Event 2").first())

    def test_event_service_get_event(self):
        event = Event.objects.create(**self.event_data2)
        retrieved_event = EventService.get_event(event.id)
        self.assertEqual(retrieved_event.name, "Service Test Event 2")
        self.assertEqual(retrieved_event.AppName, "ServiceTestApp2")
        self.assertEqual(
            retrieved_event.description, "This is another service test event."
        )
        self.assertEqual(retrieved_event.location, "Service Test Location 2")
        self.assertEqual(retrieved_event.timezone, "UTC")
        self.assertEqual(str(retrieved_event.start_date), "2023-10-03 09:00:00+00:00")
        self.assertEqual(str(retrieved_event.end_date), "2023-10-04 18:00:00+00:00")
        self.assertEqual(
            str(retrieved_event.hacker_deadline), "2023-09-29 23:59:59+00:00"
        )
        self.assertEqual(
            str(retrieved_event.mentor_deadline), "2023-09-30 23:59:59+00:00"
        )
        self.assertEqual(
            str(retrieved_event.volunteer_deadline), "2023-10-01 23:59:59+00:00"
        )
        self.assertEqual(
            str(retrieved_event.sponsor_deadline), "2023-10-02 23:59:59+00:00"
        )
        self.assertEqual(
            retrieved_event.terms_and_conditions_link, "https://example.com/terms2"
        )

    def test_event_service_get_firt_100_events(self):
        events = EventService.get_first_100_events()
        self.assertEqual(events.count(), 1)
        self.assertIn(self.event, events)

    def test_update_event(self):
        updated_data = self.event_data.copy()
        updated_data["name"] = "Updated Test Event"
        updated_data["AppName"] = "UpdatedTestApp"
        updated_event = EventService.update_event(self.event.id, updated_data)

        self.assertEqual(updated_event.name, "Updated Test Event")
        self.assertEqual(updated_event.AppName, "UpdatedTestApp")

    def test_delete_event(self):
        EventService.delete_event(self.event.id)

        events = EventService.get_first_100_events()
        self.assertEqual(events.count(), 0)

    def test_find_by_name_and_appName(self):
        search = "UnknownName"
        events = EventService.find_by_name_and_appName(search)
        self.assertEqual(events.count(), 0)

        search = "TestApp"
        events = EventService.find_by_name_and_appName(search)
        self.assertEqual(events.count(), 1)
        self.assertEqual(events.first().name, "Service Test Event")
        self.assertEqual(events.first().AppName, "ServiceTestApp")

        search = "Service Test Event"
        events = EventService.find_by_name_and_appName(search)
        self.assertEqual(events.count(), 1)
        self.assertEqual(events.first().name, "Service Test Event")
        self.assertEqual(events.first().AppName, "ServiceTestApp")

    def test_get_opened_applications(self):
        opened_applications = EventService.get_opened_applications(self.event.id)
        self.assertFalse(opened_applications["hacker_applications"])
        self.assertFalse(opened_applications["mentor_applications"])
        self.assertFalse(opened_applications["sponsor_applications"])
        self.assertFalse(opened_applications["volunteer_applications"])

        self.event.end_date = "2026-10-03T18:00:00Z"
        self.event.hacker_deadline = "2026-10-01T23:59:59Z"
        self.event.save()
        opened_applications = EventService.get_opened_applications(self.event.id)
        self.assertTrue(opened_applications["hacker_applications"])
        self.assertFalse(opened_applications["mentor_applications"])
        self.assertFalse(opened_applications["sponsor_applications"])
        self.assertFalse(opened_applications["volunteer_applications"])

        self.event.mentor_deadline = "2026-10-01T23:59:59Z"
        self.event.save()
        opened_applications = EventService.get_opened_applications(self.event.id)
        self.assertTrue(opened_applications["hacker_applications"])
        self.assertTrue(opened_applications["mentor_applications"])
        self.assertFalse(opened_applications["sponsor_applications"])
        self.assertFalse(opened_applications["volunteer_applications"])

        self.event.sponsor_deadline = "2026-10-01T23:59:59Z"
        self.event.save()
        opened_applications = EventService.get_opened_applications(self.event.id)
        self.assertTrue(opened_applications["hacker_applications"])
        self.assertTrue(opened_applications["mentor_applications"])
        self.assertTrue(opened_applications["sponsor_applications"])
        self.assertFalse(opened_applications["volunteer_applications"])

        self.event.volunteer_deadline = "2026-10-01T23:59:59Z"
        self.event.save()
        opened_applications = EventService.get_opened_applications(self.event.id)
        self.assertTrue(opened_applications["hacker_applications"])
        self.assertTrue(opened_applications["mentor_applications"])
        self.assertTrue(opened_applications["sponsor_applications"])
        self.assertTrue(opened_applications["volunteer_applications"])

    def test_service_event_to_dict(self):
        event_dict = EventService.event_to_dict(self.event)
        print(event_dict)
        self.assertIn(self.event.name, event_dict[0].values())
        self.assertIn(self.event.AppName, event_dict[1].values())
        self.assertIn(self.event.description, event_dict[2].values())
        self.assertIn(self.event.location, event_dict[3].values())
        self.assertIn(
            "GMT+0", event_dict[4].values()
        )  # This is the value for the timezone UTC in the timezoneEnum
        self.assertIn(str(self.event.start_date), event_dict[5].values())
        self.assertIn(str(self.event.end_date), event_dict[6].values())
        self.assertIn(None, event_dict[7].values())
        self.assertIn(None, event_dict[8].values())
        self.assertIn(None, event_dict[9].values())
        self.assertIn(None, event_dict[10].values())
        self.assertIn(None, event_dict[11].values())
        self.assertIn(self.event.terms_and_conditions_link, event_dict[12].values())


class ViewsEventTestCase(TestCase):
    """
    Test case for the Event views.
    """

    def setUp(self):
        self.event = Event.objects.create(
            **{
                "name": "View Test Event",
                "AppName": "ViewTestApp",
                "description": "This is a view test event.",
                "location": "View Test Location",
                "timezone": "UTC",
                "start_date": "2023-10-01T09:00:00Z",
                "end_date": "2023-10-02T18:00:00Z",
                "hacker_deadline": "2023-09-25T23:59:59Z",
                "mentor_deadline": "2023-09-26T23:59:59Z",
                "volunteer_deadline": "2023-09-27T23:59:59Z",
                "sponsor_deadline": "2023-09-28T23:59:59Z",
                "terms_and_conditions_link": "https://example.com/terms",
            }
        )
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

        self.event_data = {
            "name": "Service Test Event",
            "AppName": "ServiceTestApp",
            "description": "This is a service test event.",
            "location": "Service Test Location",
            "timezone": "UTC",
            "start_date": "2023-10-01T09:00:00Z",
            "end_date": "2023-10-02T18:00:00Z",
            "hacker_deadline": "2023-09-25T23:59:59Z",
            "mentor_deadline": "2023-09-26T23:59:59Z",
            "volunteer_deadline": "2023-09-27T23:59:59Z",
            "sponsor_deadline": "2023-09-28T23:59:59Z",
            "terms_and_conditions_link": "https://example.com/terms",
        }

        self.event_data2 = {
            "name": "Service Test Event 2",
            "AppName": "ServiceTestApp2",
            "description": "This is another service test event.",
            "location": "Service Test Location 2",
            "timezone": "UTC",
            "start_date": "2023-10-03T09:00:00Z",
            "end_date": "2023-10-04T18:00:00Z",
            "hacker_deadline": "2023-09-29T23:59:59Z",
            "mentor_deadline": "2023-09-30T23:59:59Z",
            "volunteer_deadline": "2023-10-01T23:59:59Z",
            "sponsor_deadline": "2023-10-02T23:59:59Z",
            "terms_and_conditions_link": "https://example.com/terms2",
        }

    def test_event_view_get(self):
        """
        Test method to get the EventView GET request.
        """
        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get("/event/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events.html")
        self.assertEqual(len(response.context["events"]), 1)
        self.assertIn(self.event, response.context["events"])

        response = self.client.get("/event/?search=NonExistentEvent")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events.html")
        self.assertEqual(len(response.context["events"]), 0)

    def test_event_CRUD_view_get(self):
        """
        Test the EventCRUDView GET method for loading an event.
        """
        response = self.client.get("/event/00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 403)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get("/event/00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"/event/{self.event.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eventDetail.html")

        Admin.objects.create(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user1,
        )

        response = self.client.get(f"/event/{self.event.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eventUpdate.html")

    def test_event_CRUD_view_post(self):
        """
        Test the EventCRUDView POST method for updating events.
        """
        response = self.client.post("/event/00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 403)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post("/event/00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f"/event/{self.event.id}/")
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "eventUpdate.html")

        response = self.client.post(f"/event/{self.event.id}/", self.event_data)
        self.assertEqual(response.status_code, 403)

        Admin.objects.create(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user1,
        )

        response = self.client.post(f"/event/{self.event.id}/", self.event_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eventUpdate.html")

    def test_event_CRUD_view_delete(self):
        """
        Test the EventCRUDView DELETE method for deleting events.
        """
        response = self.client.delete("/event/00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.delete("/event/00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f"/event/{self.event.id}/")
        self.assertEqual(response.status_code, 403)

        Admin.objects.create(
            phone_number="123456789",
            type="ADMIN",
            accepted_terms_and_conditions=True,
            t_shirt_size="M",
            origin="Spain",
            status="Under Review",
            event=self.event,
            user=self.user1,
        )

        response = self.client.delete(f"/event/{self.event.id}/")
        self.assertEqual(response.status_code, 204)

    def test_event_creation_view_get(self):
        """
        Test the EventCreationView GET method for rendering the event creation form.
        """
        response = self.client.get("/event/create/")
        self.assertEqual(response.status_code, 403)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get("/event/create/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eventCreation.html")

    def test_event_creation_view_post(self):
        """
        Test the EventCreationView POST method for creating a new event.
        """
        response = self.client.post("/event/create/")
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/event/create/", self.event_data)
        self.assertEqual(response.status_code, 403)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post("/event/create/", self.event_data)
        self.assertEqual(response.status_code, 302)

        response = self.client.post("/event/create/", self.event_data)
        self.assertEqual(response.status_code, 400)

        response = self.client.post("/event/create/", self.event_data2)
        self.assertEqual(response.status_code, 302)
