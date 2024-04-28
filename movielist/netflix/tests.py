from django.test import TestCase
from http import HTTPStatus
from copy import deepcopy

from django.contrib.auth.models import User
from django.contrib import auth

from netflix.models import Category, Movie



TEST_DATA = {
    "firstname": "alizh",
    "lastname": "hope",
    "email": "a_serkeshev@kbtu.kz",
    "password": "As28012005",
    "password_conf": "As28012005"
}


class IndexTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Action")
        self.spider_man_movie = Movie.objects.create(
            name="Spider man",
            category=self.category
        )
        self.avatar_movie = Movie.objects.create(
            name="Avatar",
            category=self.category
        )

    def test_index_render_all_movies(self):
        response = self.client.get("/")
        self.assertContains(response, self.spider_man_movie.name)
        self.assertContains(response, self.avatar_movie.name)

    def test_index_filter_movies(self):
        response = self.client.post("/",
        data={"search_text": "avat"}
    )
        self.assertContains(response, self.avatar_movie.name)
        self.assertNotContains(response, self.spider_man_movie.name)

class RegisterTests(TestCase):
    def test_get_registration_page(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
        response,
        '<button type="submit">Register</button>',
        html=True
    )
    def test_registration_with_valid_data(self):
        self.assertEqual(User.objects.count(), 0)
        self.client.post("/register", data=TEST_DATA)
        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.first_name, TEST_DATA['firstname'])
        self.assertEqual(new_user.last_name, TEST_DATA['lastname'])
        self.assertEqual(new_user.email, TEST_DATA['email'])
    def test_registration_with_empty_fields(self):
        self.assertEqual(User.objects.count(), 0)
        response = self.client.post(
        "/register",
        data={
            "firstname": "",
            "lastname": "",
            "email": "",
            "password": "",
            "password_conf": ""
        }
    )
        self.assertEqual(User.objects.count(), 0)
        self.assertContains(response, 'This field is required')
    def test_registration_with_wrong_password_confirmation(self):
        self.assertEqual(User.objects.count(), 0)
        bad_data = deepcopy(TEST_DATA)
        bad_data['password_conf'] = "Wrong Password Confirmation"
        response = self.client.post(
        "/register",
        data=bad_data
    )
        self.assertEqual(User.objects.count(), 0)
        self.assertContains(response, 'wrong confirmation')

class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="a_serkeshev@kbtu.kz")
        self.user_password = "As28012005"
        self.user.set_password(self.user_password)
        self.user.save()

    def test_login_with_invalid_credentials(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        response = self.client.post("/login",
        data={"email": self.user.username, "password": "Wrong password"}
    )
        self.assertContains(response, 'Invalid credentials.')
        self.assertFalse(auth.get_user(self.client).is_authenticated)

    def test_login_with_good_credentials(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        self.client.post("/login",
        data={"email": self.user.username, "password": self.user_password}
    )
        self.assertTrue(auth.get_user(self.client).is_authenticated)


