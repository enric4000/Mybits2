from django.forms import ValidationError
from django.test import TestCase

from Apps.event.models import Event
from Apps.participant.Enums.participantTypeEnum import ParticipantTypeEnum
from Apps.participant.forms import (
    AdminForm,
    HackerForm,
    MentorForm,
    SponsorForm,
    VolunteerForm,
)
from Apps.participant.models import Admin, Hacker, Mentor, Sponsor, Volunteer
from Apps.participant.services import ParticipantService
from Apps.users.models import CustomUser
from django.test import RequestFactory


# Create your tests here.
class ModelParticipantTestCase(TestCase):
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

        self.mentor_data = {
            "accepted_date": None,
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
            "accepted_date": None,
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
            "accepted_date": None,
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
            "accepted_date": None,
            "application_date": "2000-01-01",
            "phone_number": "+1234567890",
            "type": "Admin",
            "accepted_terms_and_conditions": True,
            "t_shirt_size": "M",
            "origin": "Spain",
            "status": "Under Review",
        }

    def test_participant_creation(self):
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.clean()
        hacker.save()
        self.assertIsNotNone(Hacker.objects.all())

        mentor = Mentor(**self.mentor_data, user=self.user1, event=self.event)
        mentor.clean()
        mentor.save()
        self.assertIsNotNone(Mentor.objects.all())

        sponsor = Sponsor(**self.sponsor_data, user=self.user1, event=self.event)
        sponsor.clean()
        sponsor.save()
        self.assertIsNotNone(Sponsor.objects.all())

        volunteer = Volunteer(**self.volunteer_data, user=self.user1, event=self.event)
        volunteer.clean()
        volunteer.save()
        self.assertIsNotNone(Volunteer.objects.all())

        admin = Admin(**self.admin_data, user=self.user1, event=self.event)
        admin.clean()
        admin.save()
        self.assertIsNotNone(Admin.objects.all())

    def test_participant_incorrect_data_creation(self):
        with self.assertRaises(ValidationError):
            hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
            hacker.type = "InvalidType"
            hacker.graduation_year = None
            hacker.clean()
            hacker.save()

        with self.assertRaises(ValidationError):
            mentor = Mentor(**self.mentor_data, user=self.user1, event=self.event)
            mentor.type = "InvalidType"
            mentor.degree = None
            mentor.university = None
            mentor.clean()
            mentor.save()

        with self.assertRaises(ValidationError):
            sponsor = Sponsor(**self.sponsor_data, user=self.user1, event=self.event)
            sponsor.type = "InvalidType"
            sponsor.clean()
            sponsor.save()

        with self.assertRaises(ValidationError):
            volunteer = Volunteer(
                **self.volunteer_data, user=self.user1, event=self.event
            )
            volunteer.type = "InvalidType"
            volunteer.clean()
            volunteer.save()

        with self.assertRaises(ValidationError):
            admin = Admin(**self.admin_data, user=self.user1, event=self.event)
            admin.type = "InvalidType"
            admin.clean()
            admin.save()

        with self.assertRaises(ValidationError):
            admin = Admin(**self.admin_data, user=self.user1, event=self.event)
            admin.accepted_terms_and_conditions = False
            admin.phone_number = "abcde"
            admin.clean()
            admin.save()


class ServiceParticipantTestCase(TestCase):
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
            domain_link="http://a.com",
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
            "english_level": "LOW",
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

    def test_create_participant(self):
        form = AdminForm(self.admin_data)
        form.type = ParticipantTypeEnum.ADMIN
        form.is_valid()
        admin = ParticipantService.create_participant(form, self.event, self.user1)
        self.assertIsNotNone(admin)

        form = HackerForm(self.hacker_data)
        form.type = ParticipantTypeEnum.HACKER
        form.is_valid()

        with self.assertRaises(ValidationError):
            hacker = ParticipantService.create_participant(form, self.event, self.user1)

        admin.delete()
        hacker = ParticipantService.create_participant(form, self.event, self.user1)
        self.assertIsNotNone(hacker)

        hacker.delete()
        form = MentorForm(self.mentor_data)
        form.type = ParticipantTypeEnum.MENTOR
        form.is_valid()
        mentor = ParticipantService.create_participant(form, self.event, self.user1)
        self.assertIsNotNone(mentor)

        mentor.delete()
        form = SponsorForm(self.sponsor_data)
        form.type = ParticipantTypeEnum.SPONSOR
        form.is_valid()
        sponsor = ParticipantService.create_participant(form, self.event, self.user1)
        self.assertIsNotNone(sponsor)

        sponsor.delete()
        form = VolunteerForm(self.volunteer_data)
        form.type = ParticipantTypeEnum.VOLUNTEER
        form.is_valid()
        volunteer = ParticipantService.create_participant(form, self.event, self.user1)
        self.assertIsNotNone(volunteer)

    def test_update_participant(self):
        """
        Test updating an existing participant
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        form = HackerForm({**self.hacker_data, "origin": "Updated Hacker Origin"})
        form.type = ParticipantTypeEnum.HACKER
        form.is_valid()
        updated_hacker = ParticipantService.update_participant(
            hacker, form, self.event, self.user1
        )
        self.assertEqual(updated_hacker.origin, "Updated Hacker Origin")
        self.assertEqual(updated_hacker.user, self.user1)
        self.assertEqual(updated_hacker.event, self.event)

        mentor = Mentor(**self.mentor_data, user=self.user1, event=self.event)
        mentor.save()
        form = MentorForm({**self.mentor_data, "origin": "Updated Mentor Origin"})
        form.type = ParticipantTypeEnum.MENTOR
        form.is_valid()
        updated_mentor = ParticipantService.update_participant(
            mentor, form, self.event, self.user1
        )
        self.assertEqual(updated_mentor.origin, "Updated Mentor Origin")
        self.assertEqual(updated_mentor.user, self.user1)
        self.assertEqual(updated_mentor.event, self.event)

        sponsor = Sponsor(**self.sponsor_data, user=self.user1, event=self.event)
        sponsor.save()
        form = SponsorForm({**self.sponsor_data, "origin": "Updated Sponsor Origin"})
        form.type = ParticipantTypeEnum.SPONSOR
        form.is_valid()
        updated_sponsor = ParticipantService.update_participant(
            sponsor, form, self.event, self.user1
        )
        self.assertEqual(updated_sponsor.origin, "Updated Sponsor Origin")
        self.assertEqual(updated_sponsor.user, self.user1)
        self.assertEqual(updated_sponsor.event, self.event)

        volunteer = Volunteer(**self.volunteer_data, user=self.user1, event=self.event)
        volunteer.save()
        form = VolunteerForm(
            {**self.volunteer_data, "origin": "Updated Volunteer Origin"}
        )
        form.type = ParticipantTypeEnum.VOLUNTEER
        form.is_valid()
        updated_volunteer = ParticipantService.update_participant(
            volunteer, form, self.event, self.user1
        )
        self.assertEqual(updated_volunteer.origin, "Updated Volunteer Origin")
        self.assertEqual(updated_volunteer.user, self.user1)
        self.assertEqual(updated_volunteer.event, self.event)

        admin = Admin(**self.admin_data, user=self.user1, event=self.event)
        admin.save()
        form = AdminForm({**self.admin_data, "origin": "Updated Admin Origin"})
        form.type = ParticipantTypeEnum.ADMIN
        form.is_valid()
        updated_admin = ParticipantService.update_participant(
            admin, form, self.event, self.user1
        )
        self.assertEqual(updated_admin.origin, "Updated Admin Origin")
        self.assertEqual(updated_admin.user, self.user1)
        self.assertEqual(updated_admin.event, self.event)

    def test_delete_participant(self):
        """
        Test deleting an existing participant
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        ParticipantService.delete_participant(hacker)
        self.assertEqual(Hacker.objects.count(), 0)

        mentor = Mentor(**self.mentor_data, user=self.user1, event=self.event)
        mentor.save()
        ParticipantService.delete_participant(mentor)
        self.assertEqual(Mentor.objects.count(), 0)

        sponsor = Sponsor(**self.sponsor_data, user=self.user1, event=self.event)
        sponsor.save()
        ParticipantService.delete_participant(sponsor)
        self.assertEqual(Sponsor.objects.count(), 0)

        volunteer = Volunteer(**self.volunteer_data, user=self.user1, event=self.event)
        volunteer.save()
        ParticipantService.delete_participant(volunteer)
        self.assertEqual(Volunteer.objects.count(), 0)

        admin = Admin(**self.admin_data, user=self.user1, event=self.event)
        admin.save()
        ParticipantService.delete_participant(admin)
        self.assertEqual(Admin.objects.count(), 0)

    def test_get_event_participants(self):
        """
        Test getting all participants for an event
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        mentor = Mentor(**self.mentor_data, user=self.user1, event=self.event)
        mentor.save()
        sponsor = Sponsor(**self.sponsor_data, user=self.user1, event=self.event)
        sponsor.save()
        volunteer = Volunteer(**self.volunteer_data, user=self.user1, event=self.event)
        volunteer.save()
        admin = Admin(**self.admin_data, user=self.user1, event=self.event)
        admin.save()

        participants = ParticipantService.get_event_participants(self.event)
        self.assertEqual(len(participants), 5)

    def test_filter_by_name_and_email(self):
        """
        Test filtering participants by name and email
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        filtered_participants = ParticipantService.filter_by_name_and_email(
            "albert", ParticipantService.get_event_participants(self.event)
        )
        self.assertEqual(len(filtered_participants), 1)

        filtered_participants = ParticipantService.filter_by_name_and_email(
            "nonexistent", ParticipantService.get_event_participants(self.event)
        )
        self.assertEqual(len(filtered_participants), 0)

    def test_filter_event_participants_by_type(self):
        """
        Test filtering participants by type
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        mentor = Mentor(**self.mentor_data, user=self.user1, event=self.event)
        mentor.save()
        sponsor = Sponsor(**self.sponsor_data, user=self.user1, event=self.event)
        sponsor.save()
        volunteer = Volunteer(**self.volunteer_data, user=self.user1, event=self.event)
        volunteer.save()
        admin = Admin(**self.admin_data, user=self.user1, event=self.event)
        admin.save()

        filtered_participants = ParticipantService.filter_event_participants_by_type(
            "Hacker", ParticipantService.get_event_participants(self.event)
        )
        self.assertEqual(len(filtered_participants), 1)

        filtered_participants = ParticipantService.filter_event_participants_by_type(
            "Mentor", ParticipantService.get_event_participants(self.event)
        )
        self.assertEqual(len(filtered_participants), 1)

        filtered_participants = ParticipantService.filter_event_participants_by_type(
            "Sponsor", ParticipantService.get_event_participants(self.event)
        )
        self.assertEqual(len(filtered_participants), 1)

        filtered_participants = ParticipantService.filter_event_participants_by_type(
            "Volunteer", ParticipantService.get_event_participants(self.event)
        )
        self.assertEqual(len(filtered_participants), 1)

        filtered_participants = ParticipantService.filter_event_participants_by_type(
            "Admin", ParticipantService.get_event_participants(self.event)
        )
        self.assertEqual(len(filtered_participants), 1)

    def test_get_participant_by_status(self):
        """
        Test getting participants by status
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        mentor = Mentor(**self.mentor_data, user=self.user1, event=self.event)
        mentor.save()
        sponsor = Sponsor(**self.sponsor_data, user=self.user1, event=self.event)
        sponsor.save()
        volunteer = Volunteer(**self.volunteer_data, user=self.user1, event=self.event)
        volunteer.save()
        admin = Admin(**self.admin_data, user=self.user1, event=self.event)
        admin.save()

        under_review_participants = (
            ParticipantService.filter_event_participants_by_status(
                "Under Review", ParticipantService.get_event_participants(self.event)
            )
        )
        self.assertEqual(len(under_review_participants), 5)

        accepted_participants = ParticipantService.filter_event_participants_by_status(
            "Accepted", ParticipantService.get_event_participants(self.event)
        )
        self.assertEqual(len(accepted_participants), 0)
        rejected_participants = ParticipantService.filter_event_participants_by_status(
            "Rejected", ParticipantService.get_event_participants(self.event)
        )
        self.assertEqual(len(rejected_participants), 0)
        waitlisted_participants = (
            ParticipantService.filter_event_participants_by_status(
                "Waitlisted", ParticipantService.get_event_participants(self.event)
            )
        )
        self.assertEqual(len(waitlisted_participants), 0)

    def test_get_participant(self):
        """
        Test getting a participant by ID
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        retrieved_hacker = ParticipantService.get_participant(self.event.id, hacker.id)
        self.assertEqual(retrieved_hacker, hacker)

        mentor = Mentor(**self.mentor_data, user=self.user1, event=self.event)
        mentor.save()
        retrieved_mentor = ParticipantService.get_participant(self.event.id, mentor.id)
        self.assertEqual(retrieved_mentor, mentor)

        sponsor = Sponsor(**self.sponsor_data, user=self.user1, event=self.event)
        sponsor.save()
        retrieved_sponsor = ParticipantService.get_participant(
            self.event.id, sponsor.id
        )
        self.assertEqual(retrieved_sponsor, sponsor)

        volunteer = Volunteer(**self.volunteer_data, user=self.user1, event=self.event)
        volunteer.save()
        retrieved_volunteer = ParticipantService.get_participant(
            self.event.id, volunteer.id
        )
        self.assertEqual(retrieved_volunteer, volunteer)

        admin = Admin(**self.admin_data, user=self.user1, event=self.event)
        admin.save()
        retrieved_admin = ParticipantService.get_participant(self.event.id, admin.id)
        self.assertEqual(retrieved_admin, admin)

    def test_get_participant_by_event_and_user(self):
        """
        Test getting a participant by event and user
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        retrieved_participants = ParticipantService.get_participant_by_event_and_user(
            self.event, self.user1
        )
        self.assertEqual(retrieved_participants, hacker)

    def test_get_participant_form(self):
        """
        Test getting the form for a participant
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        form = ParticipantService.get_participant_form(hacker)
        self.assertIsInstance(form, HackerForm)

        mentor = Mentor(**self.mentor_data, user=self.user1, event=self.event)
        mentor.save()
        form = ParticipantService.get_participant_form(mentor)
        self.assertIsInstance(form, MentorForm)

        sponsor = Sponsor(**self.sponsor_data, user=self.user1, event=self.event)
        sponsor.save()
        form = ParticipantService.get_participant_form(sponsor)
        self.assertIsInstance(form, SponsorForm)

        volunteer = Volunteer(**self.volunteer_data, user=self.user1, event=self.event)
        volunteer.save()
        form = ParticipantService.get_participant_form(volunteer)
        self.assertIsInstance(form, VolunteerForm)

        admin = Admin(**self.admin_data, user=self.user1, event=self.event)
        admin.save()
        form = ParticipantService.get_participant_form(admin)
        self.assertIsInstance(form, AdminForm)

    def test_get_request_form(self):
        """
        Test getting the request form for a participant type and request
        """

        factory = RequestFactory()

        # Test for hacker
        request = factory.post("/", data=self.hacker_data)
        form = ParticipantService.get_request_form("hacker", request)
        self.assertIsInstance(form, HackerForm)
        self.assertEqual(form.type, ParticipantTypeEnum.HACKER)

        # Test for mentor
        request = factory.post("/", data=self.mentor_data)
        form = ParticipantService.get_request_form("mentor", request)
        self.assertIsInstance(form, MentorForm)

        # Test for volunteer
        request = factory.post("/", data=self.volunteer_data)
        form = ParticipantService.get_request_form("volunteer", request)
        self.assertIsInstance(form, VolunteerForm)
        self.assertEqual(form.type, ParticipantTypeEnum.VOLUNTEER)

        # Test for sponsor
        request = factory.post("/", data=self.sponsor_data)
        form = ParticipantService.get_request_form("sponsor", request)
        self.assertIsInstance(form, SponsorForm)
        self.assertEqual(form.type, ParticipantTypeEnum.SPONSOR)

        # Test for admin
        request = factory.post("/", data=self.admin_data)
        form = ParticipantService.get_request_form("admin", request)
        self.assertIsInstance(form, AdminForm)
        self.assertEqual(form.type, ParticipantTypeEnum.ADMIN)

    def test_get_type_form(self):
        """
        Test getting the form for a participant type
        """
        form = ParticipantService.get_type_form("hacker")
        self.assertIsInstance(form, HackerForm)

        form = ParticipantService.get_type_form("mentor")
        self.assertIsInstance(form, MentorForm)

        form = ParticipantService.get_type_form("sponsor")
        self.assertIsInstance(form, SponsorForm)

        form = ParticipantService.get_type_form("volunteer")
        self.assertIsInstance(form, VolunteerForm)

        form = ParticipantService.get_type_form("admin")
        self.assertIsNone(form)

    def test_is_user_admin(self):
        """
        Test checking if a user is an admin
        """
        admin = Admin(**self.admin_data, user=self.user1, event=self.event)
        admin.save()
        self.assertTrue(ParticipantService.is_user_admin(self.event, self.user1))

        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        admin.delete()
        self.assertFalse(ParticipantService.is_user_admin(self.event, self.user1))

    def test_get_participant_admin(self):
        """
        Test getting the admin participant for a user
        """
        admin = Admin(**self.admin_data, user=self.user1, event=self.event)
        admin.save()
        retrieved_admin = ParticipantService.get_participant_admin(
            self.event, self.user1
        )
        self.assertEqual(retrieved_admin, admin)

        admin.delete()
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        retrieved_admin = ParticipantService.get_participant_admin(
            self.event, self.user1
        )
        self.assertIsNone(retrieved_admin)

    def test_is_email_in_admin_domain(self):
        """
        Test checking if an email is in the admin domain
        """
        self.assertTrue(
            ParticipantService.is_email_in_admin_domain(self.event, self.user1)
        )

        self.user1.email = "b@b.com"
        self.assertFalse(
            ParticipantService.is_email_in_admin_domain(self.event, self.user1)
        )

    def test_participant_to_dict(self):
        """
        Test converting a participant to a dictionary
        """
        admin = Admin(**self.admin_data, user=self.user1, event=self.event)
        admin.save()
        admin_dict = ParticipantService.participant_to_dict(admin)
        self.assertIn("Admin", str(admin_dict))

    def test_create_default_admin(self):
        """
        Test creating a default admin participant
        """
        admin = ParticipantService.create_default_admin(self.event, self.user1)
        self.assertIsNotNone(admin)
        self.assertEqual(admin.user, self.user1)
        self.assertEqual(admin.event, self.event)
        self.assertEqual(admin.type, "ADMIN")

    def test_is_participant_accepted_or_attended(self):
        """
        Test checking if a participant is accepted or attended
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        self.assertFalse(ParticipantService.is_participant_accepted_or_attended(hacker))

        hacker.status = "Confirmed"
        hacker.save()
        self.assertTrue(ParticipantService.is_participant_accepted_or_attended(hacker))

        hacker.status = "Attended"
        hacker.save()
        self.assertTrue(ParticipantService.is_participant_accepted_or_attended(hacker))

        hacker.status = "Rejected"
        hacker.save()
        self.assertFalse(ParticipantService.is_participant_accepted_or_attended(hacker))

    def test_check_in_participant(self):
        """
        Test checking in a participant
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        self.assertTrue(ParticipantService.check_in_participant(hacker))

        self.assertFalse(ParticipantService.check_in_participant(hacker))

    def test_is_participant_under_review(self):
        """
        Test checking if a participant is under review
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        self.assertTrue(ParticipantService.is_participant_under_review(hacker))

        hacker.status = "Confirmed"
        hacker.save()
        self.assertFalse(ParticipantService.is_participant_under_review(hacker))

        hacker.status = "Rejected"
        hacker.save()
        self.assertFalse(ParticipantService.is_participant_under_review(hacker))
        hacker.status = "Waitlisted"
        hacker.save()
        self.assertFalse(ParticipantService.is_participant_under_review(hacker))
        hacker.status = "Attended"
        hacker.save()
        self.assertFalse(ParticipantService.is_participant_under_review(hacker))

    def test_accept_participant(self):
        """
        Test accepting a participant
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        self.assertTrue(ParticipantService.accept_participant(hacker))

        self.assertEqual(hacker.status, "CONFIRMED")
        self.assertIsNotNone(hacker.accepted_date)

    def test_reject_participant(self):
        """
        Test rejecting a participant
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        self.assertTrue(ParticipantService.reject_participant(hacker))

        self.assertEqual(hacker.status, "REJECTED")
        self.assertIsNone(hacker.accepted_date)

    def test_get_participant_diet(self):
        """
        Test getting the diet of a participant
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()
        self.assertEqual(ParticipantService.get_participant_diet(hacker), "NONE")

        hacker.user.dietary = "VEGETARIAN"
        hacker.save()
        self.assertEqual(ParticipantService.get_participant_diet(hacker), "VEGETARIAN")

        hacker.user.dietary_other = "VEGAN"
        hacker.save()
        self.assertEqual(ParticipantService.get_participant_diet(hacker), "VEGAN")
        hacker.user.dietary = "OTHER"
        hacker.user.dietary_other = "Vegan"
        hacker.save()
        self.assertEqual(ParticipantService.get_participant_diet(hacker), "Vegan")


class ViewParticipantTestCase(TestCase):
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
            domain_link="http://a.com",
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
        self.base_url = f"/event/{self.event.id}/participant/"

    def test_participant_view_get(self):
        """
        Test the participant view GET method
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()

        response = self.client.get(
            f"/event/00000000-0000-0000-0000-000000000000/participant/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "participants.html")

        response = self.client.get(
            f"{self.base_url}?search=albert&type=Admin&status=Under Review"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "participants.html")
        self.assertContains(response, "albert")

    def test_participant_CRUD_view_get(self):
        """
        Test the participant CRUD view GET method
        """
        hacker = Hacker(**self.hacker_data, user=self.user1, event=self.event)
        hacker.save()

        response = self.client.get(
            f"/event/00000000-0000-0000-0000-000000000000/participant/00000000-0000-0000-0000-000000000000/"
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
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.base_url}{hacker.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "participantEdit.html")

        hacker.user = self.user2
        hacker.save()

        Hacker(**self.hacker_data, user=self.user1, event=self.event).save()
        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f"{self.base_url}{hacker.id}/")
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(f"{self.base_url}{hacker.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "participantDetail.html")

    def test_participant_CRUD_view_post(self):
        """
        Test the participant CRUD view POST method
        """
        hacker = Hacker(**self.hacker_data, user=self.user2, event=self.event)
        hacker.save()

        response = self.client.post(
            f"/event/00000000-0000-0000-0000-000000000000/participant/00000000-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            f"{self.base_url}00000000-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f"{self.base_url}{hacker.id}/")
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post(f"{self.base_url}{hacker.id}/")
        self.assertEqual(response.status_code, 403)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f"{self.base_url}{hacker.id}/")
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "participantEdit.html")

        response = self.client.post(
            f"{self.base_url}{hacker.id}/", data={**self.hacker_data}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "participantEdit.html")

    def test_participant_CRUD_view_delete(self):
        """
        Test the participant CRUD view DELETE method
        """
        hacker = Hacker(**self.hacker_data, user=self.user2, event=self.event)
        hacker.save()

        response = self.client.delete(
            f"/event/00000000-0000-0000-0000-000000000000/participant/00000000-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(
            f"{self.base_url}00000000-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f"{self.base_url}{hacker.id}/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.delete(f"{self.base_url}{hacker.id}/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.delete(f"{self.base_url}{hacker.id}/")
        self.assertEqual(response.status_code, 204)

    def test_participant_application_view_get(self):
        """
        Test the participant application view GET method
        """
        hacker = Hacker(**self.hacker_data, user=self.user2, event=self.event)
        hacker.save()

        response = self.client.get(
            f"/event/00000000-0000-0000-0000-000000000000/participant/apply/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.base_url}apply/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f"{self.base_url}apply/")
        self.assertEqual(response.status_code, 302)

        hacker.delete()
        response = self.client.get(f"{self.base_url}apply/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "participantType.html")

        response = self.client.get(f"{self.base_url}apply/?type=hacker")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "participantApplication.html")

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f"{self.base_url}apply/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "participantApplication.html")

    def test_participant_application_view_post(self):
        """
        Test the participant application view POST method
        """
        hacker = Hacker(**self.hacker_data, user=self.user2, event=self.event)
        hacker.save()

        response = self.client.post(
            f"/event/00000000-0000-0000-0000-000000000000/participant/apply/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f"{self.base_url}apply/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post(f"{self.base_url}apply/")
        self.assertEqual(response.status_code, 400)

        response = self.client.post(f"{self.base_url}apply/", data={**self.hacker_data})
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            f"{self.base_url}apply/", data={**self.hacker_data, "type": "hacker"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "participantApplication.html")

    def test_participant_id_view_get(self):
        """
        Test the participant ID view GET method
        """
        hacker = Hacker(**self.hacker_data, user=self.user2, event=self.event)
        hacker.save()

        response = self.client.get(
            f"/event/00000000-0000-0000-0000-000000000000/participant/00000000-0000-0000-0000-000000000000/id/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(
            f"{self.base_url}00000000-0000-0000-0000-000000000000/id/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.base_url}{hacker.id}/id/")
        self.assertEqual(response.status_code, 403)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f"{self.base_url}{hacker.id}/id/")
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(f"{self.base_url}{hacker.id}/id/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "participantId.html")

    def test_participant_mine_id_view(self):
        """
        Test the participant mine ID view GET method
        """
        hacker = Hacker(**self.hacker_data, user=self.user2, event=self.event)
        hacker.save()

        response = self.client.get(
            f"/event/00000000-0000-0000-0000-000000000000/participant/id/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.base_url}id/")
        self.assertEqual(response.status_code, 403)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f"{self.base_url}id/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f"{self.base_url}id/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "participantId.html")

    def test_participant_mine_view(self):
        """
        Test the participant mine view GET method
        """
        hacker = Hacker(**self.hacker_data, user=self.user2, event=self.event)
        hacker.save()

        response = self.client.get(
            f"/event/00000000-0000-0000-0000-000000000000/participant/mine/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.base_url}mine/")
        self.assertEqual(response.status_code, 403)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f"{self.base_url}mine/")
        self.assertEqual(response.status_code, 400)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f"{self.base_url}mine/")
        self.assertEqual(response.status_code, 302)

    def test_participant_checkIn_view_get(self):
        """
        Test the participant check-in view GET method
        """
        hacker = Hacker(**self.hacker_data, user=self.user2, event=self.event)
        hacker.save()

        response = self.client.get(
            f"/event/00000000-0000-0000-0000-000000000000/participant/checkin/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.base_url}checkin/")
        self.assertEqual(response.status_code, 403)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.get(f"{self.base_url}checkin/")
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(f"{self.base_url}checkin/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "participantCheckIn.html")

    def test_participant_checkIn_view_post(self):
        """
        Test the participant check-in view POST method
        """
        hacker = Hacker(**self.hacker_data, user=self.user2, event=self.event)
        hacker.save()

        response = self.client.post(
            f"/event/00000000-0000-0000-0000-000000000000/participant/checkin/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f"{self.base_url}checkin/")
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            f"{self.base_url}checkin/",
            {"qrResult": "00000000-0000-0000-0000-000000000000"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(
            f"{self.base_url}checkin/",
            {"qrResult": "00000000-0000-0000-0000-000000000000"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

        self.admin.save()
        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post(
            f"{self.base_url}checkin/",
            {"qrResult": "00000000-0000-0000-0000-000000000000"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            f"{self.base_url}checkin/",
            {"qrResult": f"{hacker.id}"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

        hacker.status = "Confirmed"
        hacker.save()
        response = self.client.post(
            f"{self.base_url}checkin/",
            {"qrResult": f"{hacker.id}"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            f"{self.base_url}checkin/",
            {"qrResult": f"{hacker.id}"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 409)

    def test_participant_accept_view_post(self):
        """
        Test the participant accept view POST method
        """
        hacker = Hacker(**self.hacker_data, user=self.user2, event=self.event)
        hacker.save()

        response = self.client.post(
            f"/event/00000000-0000-0000-0000-000000000000/participant/{hacker.id}/accept/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            f"{self.base_url}00000000-0000-0000-0000-000000000000/accept/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f"{self.base_url}{hacker.id}/accept/")
        self.assertEqual(response.status_code, 401)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post(f"{self.base_url}{hacker.id}/accept/")
        self.assertEqual(response.status_code, 401)

        self.admin.save()
        response = self.client.post(f"{self.base_url}{hacker.id}/accept/")
        self.assertEqual(response.status_code, 200)

        response = self.client.post(f"{self.base_url}{hacker.id}/accept/")
        self.assertEqual(response.status_code, 403)

    def test_participant_reject_view_post(self):
        """
        Test the participant reject view POST method
        """
        hacker = Hacker(**self.hacker_data, user=self.user2, event=self.event)
        hacker.save()

        response = self.client.post(
            f"/event/00000000-0000-0000-0000-000000000000/participant/{hacker.id}/reject/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            f"{self.base_url}00000000-0000-0000-0000-000000000000/reject/"
        )
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f"{self.base_url}{hacker.id}/reject/")
        self.assertEqual(response.status_code, 401)

        self.client.login(username=self.user1.email, password=self.user1_password)
        response = self.client.post(f"{self.base_url}{hacker.id}/reject/")
        self.assertEqual(response.status_code, 401)

        self.admin.save()
        response = self.client.post(f"{self.base_url}{hacker.id}/reject/")
        self.assertEqual(response.status_code, 200)

        response = self.client.post(f"{self.base_url}{hacker.id}/reject/")
        self.assertEqual(response.status_code, 403)
