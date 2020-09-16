from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()


class Schedule(models.Model):

    available_time_slot_start = models.DateTimeField()
    available_time_slot_end = models.DateTimeField()
    user = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.get_full_name()}--{self.available_time_slot_start}-->{self.available_time_slot_end}"
