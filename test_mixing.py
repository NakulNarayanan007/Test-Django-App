import datetime

from ddf import N
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class CustomTestMixing:
    def setUp(self):
        self.user = get_user_model()
        self.temp_user = N(self.user)
        self.temp_interviewer = N(self.user)
        self.temp_pwd = "bnm789*()"
        self.test_register_url = "/accounts/register/"
        self.test_login_url = "/accounts/login/"

    def register_user(self, is_candidate, user):
        data = {
            "username": user.username,
            "email": user.email,
            "password1": self.temp_pwd,
            "password2": self.temp_pwd,
            "is_candidate": is_candidate,
        }
        return self.client.post(self.test_register_url, data, format="multipart")

    def login_user(self, username="", email="", password=""):
        return self.client.post(
            self.test_login_url,
            {"username": username, "email": email, "password": password},
            format="json",
        )

    def get_user_token(self, new_user, is_candidate):
        reg_user = self.register_user(is_candidate, new_user)
        self.current_user = self.user.objects.get(username=new_user.username)
        self.assertEqual(reg_user.status_code, status.HTTP_201_CREATED)
        data = self.login_user(new_user.username, new_user.email, self.temp_pwd)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + data.json()["key"])
        return data.json()["key"]

    def schedule_add(self, start, end):

        data = {"available_time_slot_start": start, "available_time_slot_end": end}
        return self.client.post(reverse("schedule_add"), data, format="multipart")
