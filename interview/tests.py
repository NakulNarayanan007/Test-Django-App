import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from custom_test_mixing import CustomTestMixing


class InterviewTest(CustomTestMixing, APITestCase):
    def test_schedule_add(self):
        self.get_user_token(self.temp_user, True)
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=1)
        request = self.schedule_add(start_time, end_time)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_schedule_get_success(self):
        self.get_user_token(self.temp_user, True)
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=5)
        request = self.schedule_add(start_time, end_time)

        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=3)
        self.get_user_token(self.temp_interviewer, False)
        request = self.schedule_add(start_time, end_time)
        self.current_user = self.user.objects.get(username=self.temp_user.username)
        self.current_intrw = self.user.objects.get(
            username=self.temp_interviewer.username
        )
        data = {
            "candidate_id": self.current_user.id,
            "interviewer_id ": self.current_intrw.id,
        }
        resp = self.client.post(reverse("schedule_get"), data, format="multipart")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_schedule_get_failure(self):
        self.get_user_token(self.temp_user, True)
        start_time = datetime.datetime.now() + datetime.timedelta(hours=5)
        end_time = start_time + datetime.timedelta(hours=5)
        request = self.schedule_add(start_time, end_time)

        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=3)
        self.get_user_token(self.temp_interviewer, False)
        request = self.schedule_add(start_time, end_time)
        self.current_user = self.user.objects.get(username=self.temp_user.username)
        self.current_intrw = self.user.objects.get(
            username=self.temp_interviewer.username
        )
        data = {
            "candidate_id": self.current_user.id,
            "interviewer_id ": self.current_intrw.id,
        }
        resp = self.client.post(reverse("schedule_get"), data, format="multipart")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
