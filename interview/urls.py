from django.urls import path

from interview.views import GetScheduleView, RegisterScheduleView

urlpatterns = [
    path("schedule-add/", RegisterScheduleView.as_view(), name="schedule_add"),
    path("schedule-get/", GetScheduleView.as_view(), name="schedule_get"),
]
