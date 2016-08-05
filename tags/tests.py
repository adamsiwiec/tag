from django.test import TestCase, Client
from tags.models import *
# Create your tests here.


class UserCreationTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="testcase",
                            password="password",
                            first_name="Adam",
                            last_name="Siwiec",
                            email="brick@gmail.com")

    def test_user_is_created(self):
        """User is created perfectly"""
        test = User.objects.get(username="testcase")
        self.assertEqual(test.first_name, "Adam")


class HomepageTestCase(TestCase):
    def homepage_is_up(self):
        """Homepage runs succesfully"""
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
