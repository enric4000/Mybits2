from django.test import TestCase

from Apps.users.forms import RegisterForm
from Apps.users.models import CustomUser, CustomUserManager
from Apps.users.services import UserService


# Create your tests here.
class ModelUserTestCase(TestCase):
    """
    Test case for the CustomUser model.
    """

    def setUp(self):
        """
        Set up a test user.
        """
        self.user_data1 = {
            "email": "a@a.com",
            "password": "123456AA!a",
            "username": "a",
            "first_name": "a",
            "last_name": "a",
            "gender": "MALE",
            "gender_other": "",
            "pronoun": "he/him",
            "date_of_birth": "2000-01-01",
            "dietary": "NONE",
            "dietary_other": "",
            "origin": "Spain",
        }

    def test_create(self):
        """
        Test the creation of a user.
        """
        user = CustomUser(**self.user_data1)
        user.clean()
        self.assertEqual(user.email, self.user_data1["email"])
        self.assertEqual(user.username, self.user_data1["username"])
        self.assertEqual(user.first_name, self.user_data1["first_name"])
        self.assertEqual(user.last_name, self.user_data1["last_name"])
        assert user.pk is not None

    def test_create_incorrect_other_fields(self):
        """
        Test the creation of a user.
        """
        user_data2 = self.user_data1.copy()
        user_data2["dietary_other"] = "AA"
        user_data2["gender_other"] = "AA"

        user = CustomUser(**user_data2)

        with self.assertRaises(Exception) as cm:
            user.full_clean()

        self.assertIn("gender", str(cm.exception))
        self.assertIn("dietary", str(cm.exception))

        user_data2.pop("email")
        user_data2.pop("password")

        user_manager = CustomUserManager()

        with self.assertRaises(Exception):
            user_manager.create_user(email=None, password=None, **user_data2)

            user = user_manager.create_superuser(email="a@a.com", password="", **user_data2)

class ServicesUserTestCase(TestCase):
    """
    Test case for the CustomUser model.
    """

    def setUp(self):
        """
        Set up a test user.
        """
        self.user_data1 = {
            "email": "a1@a1.com",
            "password": "123456AA!a",
            "username": "a1",
            "first_name": "a1",
            "last_name": "a1",
            "gender": "MALE",
            "gender_other": "",
            "pronoun": "he/him",
            "date_of_birth": "2000-01-01",
            "dietary": "NONE",
            "dietary_other": "",
            "origin": "Spain",
        }
        self.user1 = CustomUser.objects.create(
            email="a@a.com",
            password="123456AA!a",
            username="a",
            first_name="a",
            last_name="a",
            gender="MALE",
            gender_other="",
            pronoun="he/him",
            date_of_birth="2000-01-01",
            dietary="NONE",
            dietary_other="",
            origin="Spain",
        )
        self.user2 = CustomUser.objects.create(
            email="b@b.com",
            password="654321BB!b",
            username="b",
            first_name="b",
            last_name="b",
            gender="FEMALE",
            gender_other="",
            pronoun="she/her",
            date_of_birth="1995-05-05",
            dietary="VEGETARIAN",
            dietary_other="",
            origin="France",
        )
        self.user3 = CustomUser.objects.create(
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

    def test_get_user(self):
        """
        Test the retrieval of a user.
        """
        user = UserService.get_user(self.user1.id)
        self.assertEqual(user, self.user1)

    def test_get_first_100_users(self):
        """
        Test the retrieval of the first 100 users.
        """
        users = UserService.get_first_100_users()
        self.assertEqual(users.count(), 3)
        self.assertIn(self.user1, users)
        self.assertIn(self.user2, users)
        self.assertIn(self.user3, users)

    def test_find_by_name_and_email(self):
        """
        Test the retrieval of users by name or email.
        """
        users = UserService.find_by_name_and_email("a")
        self.assertEqual(users.count(), 1)
        self.assertIn(self.user1, users)
        self.assertNotIn(self.user2, users)
        self.assertNotIn(self.user3, users)

    def test_find_by_name_and_email_not_found(self):
        """
        Test the retrieval of users by name or email.
        """
        users = UserService.find_by_name_and_email("notfound")
        self.assertEqual(users.count(), 0)

    def test_create_user(self):
        """
        Test the creation of a user.
        """
        userForm = RegisterForm(self.user_data1)
        if userForm.is_valid():
            user = UserService.create_user(userForm)
            assert user.pk is not None
        else:
            assert False, "User form is not valid"

    def test_create_user_invalid_data(self):
        """
        Test the creation of a user.
        """
        user_data = self.user_data1.copy()
        user_data["email"] = "invalid_email"
        userForm = RegisterForm(user_data)

        with self.assertRaises(Exception):
            UserService.create_user(userForm)

    def test_update_user(self):
        """
        Test the update of a user.
        """
        user_data = self.user1.__dict__.copy()
        user_data["email"] = "new@gmail.com"
        user_data["username"] = "new"
        user_data["first_name"] = "new"
        user_data["last_name"] = "new"
        userForm = RegisterForm(user_data)
        userForm.is_valid()
        user = UserService.update_user(userForm, self.user1)
        self.assertEqual(user.email, "new@gmail.com")
        self.assertEqual(user.username, "new")
        self.assertEqual(user.first_name, "new")
        self.assertEqual(user.last_name, "new")

    def test_update_user_invalid(self):
        """
        Test the update of a user.
        """
        user_data = self.user1.__dict__.copy()
        user_data["email"] = "new"
        user_data["username"] = None
        user_data["first_name"] = None
        user_data["last_name"] = None
        userForm = RegisterForm(user_data)
        userForm.is_valid()

        with self.assertRaises(Exception):
            UserService.update_user(userForm, self.user1)


class ViewsUserTestCase(TestCase):
    def setUp(self):
        """
        Set up test users.
        """
        self.user_data1 = {
            "email": "a@a.com",
            "password": "123456AA!a",
            "username": "albert",
            "first_name": "albert",
            "last_name": "a",
            "gender": "MALE",
            "gender_other": "",
            "pronoun": "he/him",
            "date_of_birth": "2000-01-01",
            "dietary": "NONE",
            "dietary_other": "",
            "origin": "Spain",
        }
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
            password="654321BB!b",
            username="bemoll",
            first_name="bemoll",
            last_name="b",
            gender="FEMALE",
            gender_other="",
            pronoun="she/her",
            date_of_birth="1995-05-05",
            dietary="VEGETARIAN",
            dietary_other="",
            origin="France",
        )
        self.user2_password = self.user2.password
        self.user2.set_password(self.user2_password)
        self.user2.save()
        self.user3 = CustomUser.objects.create(
            email="c@c.com",
            password="abcdefCC!c",
            username="catherine",
            first_name="catherine",
            last_name="c",
            gender="OTHER",
            gender_other="Non-binary",
            pronoun="they/them",
            date_of_birth="1990-10-10",
            dietary="OTHER",
            dietary_other="Alergic to pinaple",
            origin="Germany",
        )
        self.user3_password = self.user3.password
        self.user3.set_password(self.user3_password)
        self.user3.save()

    def test_user_view_get(self):
        """
        Test the user view.
        """
        response = self.client.get("/user/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users.html")

        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)
        self.assertContains(response, self.user3.username)

    def test_user_view_with_search_get(self):
        """
        Test the user view with search.
        """
        response = self.client.get("/user/?search=a")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users.html")
        self.assertContains(response, self.user1.username)
        self.assertNotContains(response, self.user2.username)

    def test_profile_view_get(self):
        """
        Test the profile view.
        """
        response = self.client.get("/user/profile/")
        self.assertEqual(response.status_code, 302)

        self.client.login(
            username=self.user1.email,
            password=self.user1_password,
        )

        response = self.client.get("/user/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_profile_view_post(self):
        """
        Test the update profile view
        """
        self.assertTrue(
            self.client.login(
                username=self.user1.email,
                password=self.user1_password,
            )
        )

        response = self.client.post(
            "/user/profile/",
            self.user_data1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.email)
        self.assertTemplateUsed(response, "profile.html")

    def test_profile_view_delete(self):
        """
        Test the delete profile view
        """
        self.assertTrue(
            self.client.login(
                username=self.user1.email,
                password=self.user1_password,
            )
        )

        response = self.client.delete("/user/profile/")
        self.assertEqual(response.status_code, 204)
        assert not CustomUser.objects.filter(email=self.user1.email).exists()

    def test_user_profile_view_get(self):
        """
        Test the user profile view.
        """
        response = self.client.get(f"/user/{self.user1.pk}/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "userProfile.html")

    def test_custom_login_view_get(self):
        """
        Test the custom login view.
        """
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "logIn.html")

    def test_custom_login_view_post(self):
        login_start = self.client.get("/user/login/")
        token = login_start.cookies["csrftoken"].value
        login_response = self.client.post(
            "/user/login/",
            data={
                "username": self.user1.email,
                "password": self.user1_password,
            },
            HTTP_X_CSRFTOKEN=token,
            headers={"X-CSRFToken": token},
        )

        assert login_response.status_code == 302
        assert login_response.cookies["csrftoken"] is not None

    def test_custom_login_view_post_invalid(self):
        login_start = self.client.get("/user/login/")
        token = login_start.cookies["csrftoken"]

        login_response = self.client.post(
            "/user/login/",
            {"username": "AAAAA", "password": "BBBB"},
            HTTP_X_CSRFTOKEN=token,
        )
        assert login_response.status_code == 400

    def test_custom_register_view_get(self):
        """
        Test the custom register view get.
        """
        response = self.client.get("/user/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_custom_register_view_post(self):
        """
        Test the custom register view post.
        """
        response = self.client.post("/user/register/", self.user_data1)
        self.assertEqual(response.status_code, 200)
