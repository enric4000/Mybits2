from django.forms import ValidationError
from django.test import TestCase

from Apps.event.models import Event
from Apps.participant.models import Admin, Hacker
from Apps.users.models import CustomUser
from Apps.warehouse.forms import LuggageForm, WarehouseForm
from Apps.warehouse.models import Luggage, Warehouse
from Apps.warehouse.services import WarehouseService

# Create your tests here.
class ModelWarehouseTestCase(TestCase):
    """
    Test case for the warehouse and luggage models
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

    def test_luggage_creation(self):
        """
        Test creating luggage with valid data.
        """
        luggage = Luggage(
            name="Suitcase",
            description="A test suitcase",
            row_position=2,
            column_position=1,
            owner=self.hacker
        )
        luggage.save()

        self.assertIsInstance(luggage, Luggage)
        self.assertEqual(luggage.name, "Suitcase")
        self.assertEqual(luggage.description, "A test suitcase")
        self.assertEqual(luggage.row_position, 2)
        self.assertEqual(luggage.column_position, 1)
        self.assertEqual(luggage.owner, self.hacker)

    def test_luggage_incorrect_data_creation(self):
        """
        Test creating luggage with invalid data.
        """
        with self.assertRaises(ValidationError):
            luggage = Luggage(
                name="Invalid Luggage",
                description="This luggage has invalid positions",
                row_position=-1,
                column_position=0,
                owner=self.hacker
            )
            luggage.clean()
            luggage.save()

    def test_warehouse_creation(self):
        """
        Test creating a warehouse with valid data.
        """
        warehouse = Warehouse(
            name="Main Warehouse",
            rows=10,
            columns=5,
            event=self.event
        )
        warehouse.save()
        self.assertIsInstance(warehouse, Warehouse)
        self.assertEqual(warehouse.name, "Main Warehouse")
        self.assertEqual(warehouse.rows, 10)
        self.assertEqual(warehouse.columns, 5)
        self.assertEqual(warehouse.event, self.event)

    def test_warehouse_incorrect_data_creation(self):
        """
        Test creating a warehouse with invalid data.
        """
        with self.assertRaises(ValidationError):
            warehouse = Warehouse(
                name="Invalid Warehouse",
                rows=-5,
                columns=5,
                event=self.event
            )
            warehouse.clean()
            warehouse.save()

class ServiceWarehouseTestCase(TestCase):
    """
    Test case for the warehouse service
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

        self.luggage_data = {
            "name": "Test Luggage",
            "description": "A test luggage item",
            "row_position": 1,
            "column_position": 1,
            "owner": self.hacker
        }
        self.warehouse_data = {
            "name": "Test Warehouse",
            "rows": 5,
            "columns": 5,
        }

    def test_create_warehouse(self):
        """
        Test creating a new warehouse.
        """
        form = WarehouseForm(self.warehouse_data)
        form.is_valid()
        warehouse = WarehouseService.create_warehouse(form, self.event)
        self.assertIsInstance(warehouse, Warehouse)
        self.assertEqual(warehouse.name, "Test Warehouse")
        self.assertEqual(warehouse.rows, 5)
        self.assertEqual(warehouse.columns, 5)
        self.assertEqual(warehouse.event, self.event)

    def test_search_warehouse(self):
        """
        Test searching for a warehouse by name.
        """
        form = WarehouseForm(self.warehouse_data)
        form.is_valid()
        warehouse = WarehouseService.create_warehouse(form, self.event)

        searched_warehouse = WarehouseService.search_warehouses(self.event, warehouse.name)
        self.assertIn(warehouse, searched_warehouse)

        no_warehouse = WarehouseService.search_warehouses(self.event, "Nonexistent Warehouse").first()
        self.assertIsNone(no_warehouse)

    def test_get_warehouses(self):
        """
        Test retrieving all warehouses associated with an event.
        """
        form = WarehouseForm(self.warehouse_data)
        form.is_valid()
        warehouse = WarehouseService.create_warehouse(form, self.event)

        retrieved_warehouses = WarehouseService.get_warehouses(self.event)
        self.assertEqual(retrieved_warehouses.first(), warehouse)

    def test_get_warehouse(self):
        """
        Test retrieving a warehouse by its ID.
        """
        form = WarehouseForm(self.warehouse_data)
        form.is_valid()
        warehouse = WarehouseService.create_warehouse(form, self.event)

        retrieved_warehouse = WarehouseService.get_warehouse(warehouse.id)
        self.assertEqual(retrieved_warehouse, warehouse)

        with self.assertRaises(Warehouse.DoesNotExist):
            WarehouseService.get_warehouse("00000000-0000-0000-0000-000000000000")

    def test_update_warehouse(self):
        """
        Test updating an existing warehouse.
        """
        form = WarehouseForm(self.warehouse_data)
        form.is_valid()
        warehouse = WarehouseService.create_warehouse(form, self.event)

        updated_data = {
            "name": "Updated Warehouse",
            "rows": 10,
            "columns": 10,
        }
        update_form = WarehouseForm(updated_data, instance=warehouse)
        update_form.is_valid()
        updated_warehouse = WarehouseService.update_warehouse(update_form, warehouse)

        self.assertEqual(updated_warehouse.name, "Updated Warehouse")
        self.assertEqual(updated_warehouse.rows, 10)
        self.assertEqual(updated_warehouse.columns, 10)

    def test_delete_warehouse(self):
        """
        Test deleting a warehouse.
        """
        form = WarehouseForm(self.warehouse_data)
        form.is_valid()
        warehouse = WarehouseService.create_warehouse(form, self.event)

        deleted = WarehouseService.delete_warehouse(warehouse)
        self.assertTrue(deleted)
        self.assertEqual(Warehouse.objects.count(), 0)

        with self.assertRaises(Warehouse.DoesNotExist):
            WarehouseService.get_warehouse(warehouse.id)

        luggage = Luggage(**self.luggage_data)
        luggage.save()
        warehouse = WarehouseService.create_warehouse(form, self.event)
        warehouse.luggage.add(luggage)

        deleted = WarehouseService.delete_warehouse(warehouse)
        self.assertFalse(deleted)

    def test_get_warehouse_luggage(self):
        """
        Test retrieving luggage associated with a warehouse.
        """
        form = WarehouseForm(self.warehouse_data)
        form.is_valid()
        warehouse = WarehouseService.create_warehouse(form, self.event)

        luggage = Luggage(**self.luggage_data)
        luggage.save()
        warehouse.luggage.add(luggage)

        retrieved_luggage = WarehouseService.get_warehouse_luggage(warehouse)
        self.assertIn(luggage, retrieved_luggage)
        self.assertEqual(retrieved_luggage.count(), 1)

        self.assertEqual(WarehouseService.get_warehouse_luggage(None), [])

    def test_create_luggage(self):
        """
        Test creating luggage associated with a warehouse.
        """
        form = WarehouseForm(self.warehouse_data)
        form.is_valid()
        warehouse = WarehouseService.create_warehouse(form, self.event)

        form = LuggageForm(self.luggage_data)
        form.is_valid()
        luggage = WarehouseService.create_luggage(form, warehouse, self.hacker)

        self.assertIsInstance(luggage, Luggage)
        self.assertEqual(luggage.name, "Test Luggage")
        self.assertEqual(luggage.description, "A test luggage item")
        self.assertEqual(luggage.row_position, 1)
        self.assertEqual(luggage.column_position, 1)
        self.assertEqual(luggage.owner, self.hacker)

        no_luggage = WarehouseService.create_luggage(form, warehouse, self.hacker)
        self.assertIsNone(no_luggage)

        invalid_luggage_data = {
            "name": "Invalid Luggage",
            "description": "This luggage has invalid positions",
            "row_position": 1000,
            "column_position": 1000,
        }
        invalid_form = LuggageForm(invalid_luggage_data)
        invalid_form.is_valid()
        no_luggage = WarehouseService.create_luggage(invalid_form, warehouse, self.hacker)
        self.assertIsNone(no_luggage)

    def test_get_luggage(self):
        """
        Test retrieving a luggage item by its ID.
        """
        form = WarehouseForm(self.warehouse_data)
        form.is_valid()
        warehouse = WarehouseService.create_warehouse(form, self.event)

        form = LuggageForm(self.luggage_data)
        form.is_valid()
        luggage = WarehouseService.create_luggage(form, warehouse, self.hacker)

        retrieved_luggage = WarehouseService.get_luggage(luggage.id)
        self.assertEqual(retrieved_luggage, luggage)

        with self.assertRaises(Luggage.DoesNotExist):
            WarehouseService.get_luggage("00000000-0000-0000-0000-000000000000")

    def test_update_luggage(self):
        """
        Test updating an existing luggage item.
        """
        form = WarehouseForm(self.warehouse_data)
        form.is_valid()
        warehouse = WarehouseService.create_warehouse(form, self.event)

        form = LuggageForm(self.luggage_data)
        form.is_valid()
        luggage = WarehouseService.create_luggage(form, warehouse, self.hacker)

        updated_data = {
            "name": "Updated Luggage",
            "description": "An updated test luggage item",
            "row_position": 2,
            "column_position": 2,
        }
        update_form = LuggageForm(updated_data, instance=luggage)
        update_form.is_valid()
        updated_luggage = WarehouseService.update_luggage(update_form, luggage, warehouse)

        self.assertEqual(updated_luggage.name, "Updated Luggage")
        self.assertEqual(updated_luggage.description, "An updated test luggage item")
        self.assertEqual(updated_luggage.row_position, 2)
        self.assertEqual(updated_luggage.column_position, 2)
        self.assertEqual(updated_luggage.owner, self.hacker)

        invalid_data = {
            "name": "Invalid Luggage",
            "description": "This luggage has invalid positions",
            "row_position": 1000,
            "column_position": 1000,
        }
        invalid_form = LuggageForm(invalid_data, instance=luggage)
        invalid_form.is_valid()
        no_luggage = WarehouseService.update_luggage(invalid_form, luggage, warehouse)
        self.assertIsNone(no_luggage)

        no_luggage = WarehouseService.update_luggage(update_form, None, warehouse)
        self.assertIsNone(no_luggage)

    def test_delete_luggage(self):
        """
        Test deleting a luggage item.
        """
        form = WarehouseForm(self.warehouse_data)
        form.is_valid()
        warehouse = WarehouseService.create_warehouse(form, self.event)

        form = LuggageForm(self.luggage_data)
        form.is_valid()
        luggage = WarehouseService.create_luggage(form, warehouse, self.hacker)

        deleted = WarehouseService.delete_luggage(luggage, warehouse)
        self.assertTrue(deleted)
        self.assertEqual(Luggage.objects.count(), 0)

        with self.assertRaises(Luggage.DoesNotExist):
            WarehouseService.get_luggage(luggage.id)

        no_luggage = WarehouseService.delete_luggage(None, warehouse)
        self.assertFalse(no_luggage)

    def test_get_warehouse_luggage_by_participant(self):
        """
        Test retrieving luggage items by participant.
        """
        form = WarehouseForm(self.warehouse_data)
        form.is_valid()
        warehouse = WarehouseService.create_warehouse(form, self.event)

        form = LuggageForm(self.luggage_data)
        form.is_valid()
        luggage = WarehouseService.create_luggage(form, warehouse, self.hacker)

        retrieved_luggage = WarehouseService.get_warehouse_luggage_by_participant(warehouse, self.hacker)
        self.assertIn(luggage, retrieved_luggage)
        self.assertEqual(retrieved_luggage.count(), 1)

        no_luggage = WarehouseService.get_warehouse_luggage_by_participant(None, self.hacker)
        self.assertEqual(no_luggage, [])
    
        no_luggage = WarehouseService.get_warehouse_luggage_by_participant(warehouse, None)
        self.assertEqual(no_luggage, [])

class ViewWarehouseTestCase(TestCase):
    """
    Test case for the warehouse views
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

        self.luggage_data = {
            "name": "Test Luggage",
            "description": "A test luggage item",
            "row_position": 1,
            "column_position": 1,
            "owner": self.hacker
        }
        self.warehouse_data = {
            "name": "Test Warehouse",
            "rows": 5,
            "columns": 5,
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
        self.base_url = f'/event/{self.event.id}/warehouse/'

    def test_warehouse_view_get(self):
        """
        Test the warehouse list view.
        """
        warehouse =Warehouse(**self.warehouse_data, event=self.event)
        warehouse.save()

        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/warehouse/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, warehouse.name)
        self.assertTemplateUsed(response, 'warehouses.html')

        response = self.client.get(f'{self.base_url}?search=NonExistent')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, warehouse.name)
        self.assertTemplateUsed(response, 'warehouses.html')

    def test_warehouse_create_view_get(self):
        """
        Test the warehouse create view.
        """
        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/warehouse/create/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(f'{self.base_url}create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'warehouseCreate.html')

    def test_warehouse_create_view_post(self):
        """
        Test the warehouse create view.
        """
        response = self.client.post(f'/event/00000000-0000-0000-0000-000000000000/warehouse/create/', data={})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}create/', data={})
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f'{self.base_url}create/', data={})
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.post(f'{self.base_url}create/', data={})
        self.assertEqual(response.status_code, 400)
    
        response = self.client.post(f'{self.base_url}create/', data=self.warehouse_data)
        self.assertEqual(response.status_code, 302)

    def test_warehouse_CRUD_view_get(self):
        """
        Test the warehouse CRUD view.
        """
        warehouse = Warehouse(**self.warehouse_data, event=self.event)
        warehouse.save()

        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/warehouse/{warehouse.id}/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}{warehouse.id}/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f'{self.base_url}{warehouse.id}/')
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(f'{self.base_url}{warehouse.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, warehouse.name)
        self.assertTemplateUsed(response, 'warehouseEdit.html')

    def test_warehouse_CRUD_view_post(self):
        """
        Test the warehouse CRUD view.
        """
        warehouse = Warehouse(**self.warehouse_data, event=self.event)
        warehouse.save()

        response = self.client.post(f'/event/00000000-0000-0000-0000-000000000000/warehouse/{warehouse.id}/', data={})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}{warehouse.id}/', data={})
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f'{self.base_url}{warehouse.id}/', data={})
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.post(f'{self.base_url}{warehouse.id}/', data={})
        self.assertEqual(response.status_code, 400)

        updated_data = {
            "name": "Updated Warehouse",
            "rows": 10,
            "columns": 10,
        }
        response = self.client.post(f'{self.base_url}{warehouse.id}/', data=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'warehouseEdit.html')

    def test_warehouse_CRUD_view_delete(self):
        """
        Test the warehouse delete view.
        """
        warehouse = Warehouse(**self.warehouse_data, event=self.event)
        warehouse.save()

        response = self.client.delete(f'/event/00000000-0000-0000-0000-000000000000/warehouse/{warehouse.id}/')
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f'{self.base_url}{warehouse.id}/')
        self.assertEqual(response.status_code, 403)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.delete(f'{self.base_url}{warehouse.id}/')
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.delete(f'{self.base_url}{warehouse.id}/')
        self.assertEqual(response.status_code, 204)

        warehouse.save()
        luggage = Luggage(**self.luggage_data)
        luggage.save()
        warehouse.luggage.add(luggage)
        warehouse.save()
        response = self.client.delete(f'{self.base_url}{warehouse.id}/')
        self.assertEqual(response.status_code, 409)

    def test_warehouse_luggage_view_get(self):
        """
        Test the warehouse luggage view.
        """
        warehouse = Warehouse(**self.warehouse_data, event=self.event)
        warehouse.save()

        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/warehouse/{warehouse.id}/luggage/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}{warehouse.id}/luggage/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f'{self.base_url}{warehouse.id}/luggage/')
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(f'{self.base_url}{warehouse.id}/luggage/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'warehouseLuggage.html')

    def test_warehouse_luggage_create_view_get(self):
        """
        Test the warehouse luggage create view.
        """
        warehouse = Warehouse(**self.warehouse_data, event=self.event)
        warehouse.save()

        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/warehouse/{warehouse.id}/participant/00000000-0000-0000-0000-000000000000/create/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}{warehouse.id}/participant/{self.hacker.id}/create/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f'{self.base_url}{warehouse.id}/participant/{self.hacker.id}/create/')
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(f'{self.base_url}{warehouse.id}/participant/{self.hacker.id}/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'luggageCreate.html')

    def test_warehouse_luggage_create_view_post(self):
        """
        Test the warehouse luggage create view.
        """
        warehouse = Warehouse(**self.warehouse_data, event=self.event)
        warehouse.save()

        response = self.client.post(f'/event/00000000-0000-0000-0000-000000000000/warehouse/{warehouse.id}/participant/00000000-0000-0000-0000-000000000000/create/', data={})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}{warehouse.id}/participant/{self.hacker.id}/create/', data={})
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f'{self.base_url}{warehouse.id}/participant/{self.hacker.id}/create/', data={})
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.post(f'{self.base_url}{warehouse.id}/participant/{self.hacker.id}/create/', data={})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(f'{self.base_url}{warehouse.id}/participant/{self.hacker.id}/create/', data=self.luggage_data)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(f'{self.base_url}{warehouse.id}/participant/{self.hacker.id}/create/', data={
            "name": "Invalid Luggage",
            "description": "This luggage has invalid positions",
            "row_position": 1000,
            "column_position": 1000,
        })
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'luggageCreate.html')

    def test_warehouse_luggage_CRUD_view_get(self):
        """
        Test the warehouse luggage CRUD view.
        """
        warehouse = Warehouse(**self.warehouse_data, event=self.event)
        warehouse.save()

        luggage = Luggage(**self.luggage_data)
        luggage.save()
        warehouse.luggage.add(luggage)

        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/warehouse/{warehouse.id}/luggage/00000000-0000-0000-0000-000000000000/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}{warehouse.id}/luggage/00000000-0000-0000-0000-000000000000/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}{warehouse.id}/luggage/{luggage.id}/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f'{self.base_url}{warehouse.id}/luggage/{luggage.id}/')
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(f'{self.base_url}{warehouse.id}/luggage/{luggage.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, luggage.name)
        self.assertTemplateUsed(response, 'luggageEdit.html')

    def test_warehouse_luggage_CRUD_view_post(self):
        """
        Test the warehouse luggage CRUD view.
        """
        warehouse = Warehouse(**self.warehouse_data, event=self.event)
        warehouse.save()

        luggage = Luggage(**self.luggage_data)
        luggage.save()
        warehouse.luggage.add(luggage)


        response = self.client.post(f'/event/00000000-0000-0000-0000-000000000000/warehouse/{warehouse.id}/luggage/00000000-0000-0000-0000-000000000000/', data={})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}{warehouse.id}/luggage/00000000-0000-0000-0000-000000000000/', data={})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(f'{self.base_url}{warehouse.id}/luggage/{luggage.id}/', data={})
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.post(f'{self.base_url}{warehouse.id}/luggage/{luggage.id}/', data={})
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.post(f'{self.base_url}{warehouse.id}/luggage/{luggage.id}/', data={})
        self.assertEqual(response.status_code, 400)

        updated_data = {
            "name": "Updated Luggage",
            "description": "An updated test luggage item",
            "row_position": 2,
            "column_position": 2,
        }
        response = self.client.post(f'{self.base_url}{warehouse.id}/luggage/{luggage.id}/', data=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'luggageEdit.html')

    def test_warehouse_luggage_CRUD_view_delete(self):
        """
        Test the warehouse luggage delete view.
        """
        warehouse = Warehouse(**self.warehouse_data, event=self.event)
        warehouse.save()

        luggage = Luggage(**self.luggage_data)
        luggage.save()
        warehouse.luggage.add(luggage)

        response = self.client.delete(f'/event/00000000-0000-0000-0000-000000000000/warehouse/{warehouse.id}/luggage/00000000-0000-0000-0000-000000000000/')
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f'{self.base_url}{warehouse.id}/luggage/00000000-0000-0000-0000-000000000000/')
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f'{self.base_url}{warehouse.id}/luggage/{luggage.id}/')
        self.assertEqual(response.status_code, 403)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.delete(f'{self.base_url}{warehouse.id}/luggage/{luggage.id}/')
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.delete(f'{self.base_url}{warehouse.id}/luggage/{luggage.id}/')
        self.assertEqual(response.status_code, 204)

        with self.assertRaises(Luggage.DoesNotExist):
            Luggage.objects.get(id=luggage.id)

    def test_warehouse_luggage_by_participant_view_get(self):
        """
        Test the warehouse luggage by participant view.
        """
        warehouse = Warehouse(**self.warehouse_data, event=self.event)
        warehouse.save()

        luggage = Luggage(**self.luggage_data)
        luggage.save()
        warehouse.luggage.add(luggage)

        response = self.client.get(f'/event/00000000-0000-0000-0000-000000000000/warehouse/{warehouse.id}/participant/00000000-0000-0000-0000-000000000000/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f'{self.base_url}{warehouse.id}/participant/{self.hacker.id}/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user2.email, password=self.user2_password)
        response = self.client.get(f'{self.base_url}{warehouse.id}/participant/{self.hacker.id}/')
        self.assertEqual(response.status_code, 403)

        self.admin.save()
        response = self.client.get(f'{self.base_url}{warehouse.id}/participant/00000000-0000-0000-0000-000000000000/')
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'warehouseParticipant.html')

        response = self.client.get(f'{self.base_url}{warehouse.id}/participant/{self.hacker.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'warehouseLuggage.html')
