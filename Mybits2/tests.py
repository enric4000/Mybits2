from django.test import TestCase
from Apps.users.models import CustomUser


class ViewMybitsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser(
            email="c@c.com",
            password="abcdefCC!c",
            username="c",
            first_name="c",
            last_name="c",
            gender="OTHER",
            gender_other="Non-binary",
            pronoun="they/them",
            date_of_birth="1990-10-10",
            dietary="OTHER",
            dietary_other="Alergic to pinaple",
            origin="Germany",
        )
        self.user.set_password("testpassword")
        self.user.save()

    def test_home_view_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user.email, password='testpassword')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

