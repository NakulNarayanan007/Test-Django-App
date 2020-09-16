import datetime

from django.conf import settings
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from custom_test_mixing import CustomTestMixing


class AccountsTest(CustomTestMixing, APITestCase):
    def test_register_user_sucess(self):
        request = self.register_user(True, self.temp_user)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_register_user_failure(self):
        data = {
            "username": self.temp_user.username,
            "email": "",
            "password1": self.temp_user.password,
            "password2": "",
            "is_candidate": True,
        }
        request = self.client.post(self.test_register_url, data, format="multipart")
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        self.register_user(True, self.temp_user)
        request = self.login_user(
            self.temp_user.username, self.temp_user.email, self.temp_pwd
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertIn("key", request.json())

    def test_login_failure(self):
        request = self.login_user(self.temp_user.username, "", "")
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
