from django.test import TestCase

from Apps.event.models import Event
from Apps.hardware.forms import HardwareItemForm
from Apps.hardware.models import HardwareItem
from Apps.hardware.services import HardwareItemService
from Apps.participant.models import Admin, Hacker
from Apps.users.models import CustomUser

# Create your tests here.
class ModelHardwareItemTestCase(TestCase):
    """
    Test case for the HardwareItem model.
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

    def test_hardware_item_creation(self):
        hardware_item = HardwareItem(
            name="Test Hardware",
            description="This is a test hardware item.",
            quantity_available=10,
            abreviation="THW",
            event=self.event
        )
        hardware_item.borrowers.add(self.hacker)
        hardware_item.full_clean()
        hardware_item.save()
        hardware_item = HardwareItem.objects.get(name="Test Hardware")
        self.assertIsInstance(hardware_item, HardwareItem)
        self.assertEqual(hardware_item.name, "Test Hardware")
        self.assertEqual(hardware_item.description, "This is a test hardware item.")
        self.assertEqual(hardware_item.quantity_available, 10)
        self.assertEqual(hardware_item.abreviation, "THW")
        self.assertEqual(hardware_item.event, self.event)

    def test_hardware_item_creation_incorrect_data(self):
        hardware_item = HardwareItem(
            name="Test Hardware",
            description="This is a test hardware item.",
            quantity_available=-5,
            abreviation="THW",
            event=self.event
        )
        with self.assertRaises(Exception):
            hardware_item.full_clean()
            hardware_item.save()

class ServiceHardwareItemTestCase(TestCase):
    """
    Test case for the HardwareItem service.
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
        self.hacker.clean()
        self.hacker.save()

        self.hardware_data = {
            "name": "Test Hardware",
            "description": "This is a test hardware item.",
            "quantity_available": 10,
            "abreviation": "THW",
            "event": self.event
        }

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


    def test_get_hardware_items(self):
        hardware_item = HardwareItem(
            **self.hardware_data
        )
        hardware_item.borrowers.add(self.hacker)
        hardware_item.save(using='default')

        items = HardwareItemService.get_hardware_items(self.event)
        self.assertIn(hardware_item, items)
        self.assertEqual(items.count(), 1)

    def test_search_hardware_items(self):
        hardware_item = HardwareItem(
            **self.hardware_data
        )
        self.hacker.save()
        hardware_item.borrowers.add(self.hacker)
        hardware_item.full_clean()
        hardware_item.save()

        search_results = HardwareItemService.search_hardware_items(self.event, "Test")
        self.assertIn(hardware_item, search_results)
        self.assertEqual(search_results.count(), 1)

        search_results = HardwareItemService.search_hardware_items(self.event,"Nonexistent")
        self.assertNotIn(hardware_item, search_results)
        self.assertEqual(search_results.count(), 0)

    def test_available_hardware_items(self):
        hardware_item = HardwareItem(
            **self.hardware_data
        )
        self.hacker.save()
        hardware_item.borrowers.add(self.hacker)
        hardware_item.full_clean()
        hardware_item.save()

        available_items = HardwareItemService.available_hardware_items(HardwareItem.objects.all())
        self.assertIn(hardware_item, available_items)
        self.assertEqual(available_items.count(), 1)

        hardware_item.quantity_available = 0
        hardware_item.save()
        available_items = HardwareItemService.available_hardware_items(HardwareItem.objects.all())
        self.assertNotIn(hardware_item, available_items)
        self.assertEqual(available_items.count(), 0)

    def test_create_hardware_item(self):
        form = HardwareItemForm(self.hardware_data)
        hardware_item = HardwareItemService.create_hardware_item(form, self.event)
        self.assertIsInstance(hardware_item, HardwareItem)
        self.assertEqual(hardware_item.name, "Test Hardware")
        self.assertEqual(hardware_item.description, "This is a test hardware item.")
        self.assertEqual(hardware_item.quantity_available, 10)
        self.assertEqual(hardware_item.abreviation, "THW")
        self.assertEqual(hardware_item.event, self.event)

    def test_get_hardware_item(self):
        hardware_item = HardwareItem(
            **self.hardware_data
        )
        self.hacker.save()
        hardware_item.borrowers.add(self.hacker)
        hardware_item.full_clean()
        hardware_item.save()

        retrieved_item = HardwareItemService.get_hardware_item(hardware_item.id)
        self.assertEqual(retrieved_item, hardware_item)

    def test_update_hardware_item(self):
        hardware_item = HardwareItem(
            **self.hardware_data
        )
        self.hacker.save()
        hardware_item.borrowers.add(self.hacker)
        hardware_item.full_clean()
        hardware_item.save()

        updated_data = {
            "name": "Updated Hardware",
            "description": "This is an updated hardware item.",
            "quantity_available": 20,
            "abreviation": "UHW",
        }
        form = HardwareItemForm(updated_data)
        form.is_valid()
        updated_item = HardwareItemService.update_hardware_item(form, hardware_item)

        self.assertEqual(updated_item.name, "Updated Hardware")
        self.assertEqual(updated_item.description, "This is an updated hardware item.")
        self.assertEqual(updated_item.quantity_available, 20)
        self.assertEqual(updated_item.abreviation, "UHW")

    def test_delete_hardware_item(self):
        hardware_item = HardwareItem(
            **self.hardware_data
        )
        self.hacker.save()
        hardware_item.borrowers.add(self.hacker)
        hardware_item.full_clean()
        hardware_item.save()

        result = HardwareItemService.delete_hardware_item(hardware_item)
        self.assertTrue(result)
        self.assertFalse(HardwareItem.objects.filter(id=hardware_item.id).exists())

    def test_borrow_hardware_item(self):
        hardware_item = HardwareItem(
            **self.hardware_data
        )
        hardware_item.full_clean()
        hardware_item.save()

        borrowed_item = HardwareItemService.borrow_hardware_item(hardware_item, self.hacker)
        self.assertEqual(borrowed_item.quantity_available, 9)
        self.assertIn(self.hacker, borrowed_item.borrowers.all())

        null = HardwareItemService.borrow_hardware_item(hardware_item, self.hacker)
        self.assertIsNone(null)

    def test_return_hardware_item(self):
        hardware_item = HardwareItem(
            **self.hardware_data
        )
        self.hacker.save()
        hardware_item.borrowers.add(self.hacker)
        hardware_item.full_clean()
        hardware_item.save()

        HardwareItemService.borrow_hardware_item(hardware_item, self.hacker)
        returned_item = HardwareItemService.return_hardware_item(hardware_item, self.hacker)
        self.assertEqual(returned_item.quantity_available, 11)
        self.assertNotIn(self.hacker, returned_item.borrowers.all())

        null = HardwareItemService.return_hardware_item(hardware_item, self.hacker)
        self.assertFalse(null)

    def test_hardware_item_to_dict(self):
        hardware_item = HardwareItem(
            **self.hardware_data
        )
        self.hacker.save()
        hardware_item.borrowers.add(self.hacker)
        hardware_item.full_clean()
        hardware_item.save()

        item_dict = HardwareItemService.hardware_item_to_dict(hardware_item)
        self.assertIn("Test Hardware", str(item_dict[0].values()))
        self.assertIn("This is a test hardware item.", str(item_dict[1].values()))
        self.assertIn("10", str(item_dict[2].values()))
        self.assertIn("THW", str(item_dict[3].values()))

class ViewHardwareItemTestCase(TestCase):
    """
    Test case for the HardwareItem views.
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

        self.hardware_data = {
            "name": "Test Hardware",
            "description": "This is a test hardware item.",
            "quantity_available": 10,
            "abreviation": "THW",
            "event": self.event
        }
        self.hardware_item = HardwareItem(
            **self.hardware_data
        )
        self.hardware_item.save()

        self.hardware_data2 = {
            "name": "Not Available Hardware",
            "description": "This is a test hardware item.",
            "quantity_available": 0,
            "abreviation": "THW",
            "event": self.event
        }
        self.hardware_item2 = HardwareItem(
            **self.hardware_data2
        )
        self.hardware_item2.save()

        self.base_url = f'/event/{self.event.id}/hardware/'

    def test_hardware_item_view_get(self):
        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/hardware/')
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
        self.assertTemplateUsed(response, "hardwareItems.html")
        self.assertContains(response, "Test Hardware")

        response = self.client.get(f'{self.base_url}?search=algo')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hardwareItems.html")
        self.assertNotContains(response, "Test Hardware")

        self.assertTrue(self.client.login(username=self.user1.email, password=self.user1_password))
        self.hacker.save()
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hardwareItems.html")
        self.assertContains(response, "Test Hardware")
        self.assertNotContains(response, "Not Available Hardware")

    def test_hardware_item_create_view(self):
        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/hardware/create/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 403)

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

        response = self.client.get(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hardwareItemCreate.html")

    def test_hardware_item_create_view_post(self):
        response = self.client.post(f'/event/00000000-0000-0000-0000-000000000000/hardware/create/')
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 403)

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

        response = self.client.post(f'{self.base_url}create/', data={
            "name": "New Hardware",
            "description": "This is a new hardware item.",
            "quantity_available": 5,
            "abreviation": "NHW",
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post(f'{self.base_url}create/', data={
            "name": "New Hardware",
            "description": "This is a new hardware item.",
            "quantity_available": -5,
            "abreviation": "NHW",
        })
        self.assertEqual(response.status_code, 400)

    def test_hardware_item_CRUD_view_get(self):
        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/hardware/{self.hardware_item.id}/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}{self.hardware_item.id}/')
        self.assertEqual(response.status_code, 302)

        self.assertTrue(self.client.login(username=self.user1.email, password=self.user1_password))
        response = self.client.get(f'{self.base_url}{self.hardware_item.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hardwareItemDetail.html")

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
        response = self.client.get(f'{self.base_url}{self.hardware_item.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hardwareItemEdit.html")

    def test_hardware_item_CRUD_view_post(self):
        response = self.client.post(f'/event/00000000-0000-0000-0000-000000000000/hardware/{self.hardware_item.id}/')
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/')
        self.assertEqual(response.status_code, 403)

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

        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/')
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "hardwareItemEdit.html")

        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/', self.hardware_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hardwareItemEdit.html")

    def test_hardware_item_CRUD_view_delete(self):
        response = self.client.delete(f'/event/00000000-0000-0000-0000-000000000000/hardware/{self.hardware_item.id}/')
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f'{self.base_url}{self.hardware_item.id}/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.delete(f'{self.base_url}{self.hardware_item.id}/')
        self.assertEqual(response.status_code, 403)

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

        response = self.client.delete(f'{self.base_url}{self.hardware_item.id}/')
        self.assertEqual(response.status_code, 204)

    def test_hardware_item_borrow_view_get(self):
        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/hardware/{self.hardware_item.id}/borrow/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}{self.hardware_item.id}/borrow/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f'{self.base_url}{self.hardware_item.id}/borrow/')
        self.assertEqual(response.status_code, 403)

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

        response = self.client.get(f'{self.base_url}{self.hardware_item.id}/borrow/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hardwareItemBorrow.html")

    def test_hardware_item_borrow_view_post(self):
        response = self.client.post(f'/event/00000000-0000-0000-0000-000000000000/hardware/{self.hardware_item.id}/borrow/')
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/borrow/')
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/borrow/', {"qrResult":"00000000-0000-0000-0000-000000000000"})
        self.assertEqual(response.status_code, 404)

        self.hacker.save()

        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/borrow/', {"qrResult":str(self.hacker.id)},
            content_type="application/json")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/borrow/', {"qrResult":str(self.hacker.id)},
            content_type="application/json")
        self.assertEqual(response.status_code, 403)

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

        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/borrow/', {"qrResult":str(self.hacker.id)},
            content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_hardware_item_return_view_get(self):
        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/hardware/{self.hardware_item.id}/return/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}{self.hardware_item.id}/return/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f'{self.base_url}{self.hardware_item.id}/return/')
        self.assertEqual(response.status_code, 403)

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

        response = self.client.get(f'{self.base_url}{self.hardware_item.id}/return/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hardwareItemReturn.html")

    def test_hardware_item_return_view_post(self):
        response = self.client.post(f'/event/00000000-0000-0000-0000-000000000000/hardware/{self.hardware_item.id}/return/')
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/return/')
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/return/', {"qrResult":"00000000-0000-0000-0000-000000000000"})
        self.assertEqual(response.status_code, 404)

        self.hacker.save()

        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/return/', {"qrResult":str(self.hacker.id)},
            content_type="application/json")
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/return/', {"qrResult":str(self.hacker.id)},
            content_type="application/json")
        self.assertEqual(response.status_code, 403)

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

        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/return/', {"qrResult":str(self.hacker.id)},
        content_type="application/json")
        self.assertEqual(response.status_code, 400)

        self.hardware_item.borrowers.add(self.hacker)
        self.hardware_item.save()
        response = self.client.post(f'{self.base_url}{self.hardware_item.id}/return/', {"qrResult":str(self.hacker.id)},
        content_type="application/json")
        self.assertEqual(response.status_code, 200)
