from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.conf import settings
from django.contrib.auth.models import Group
from rest_auth.registration.serializers import (
    RegisterSerializer as RegisterBaseSerializer,
)
from rest_framework import serializers


class RegistrationSerializer(RegisterBaseSerializer):
    is_candidate = serializers.BooleanField(default=True)

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        # add use group here
        if self.validated_data.get("is_candidate"):
            group, _ = Group.objects.get_or_create(name=settings.CANDIDATE_GROUP_NAME)
        else:
            group, _ = Group.objects.get_or_create(name=settings.INTERVIEWER_GROUP_NAME)

        group.user_set.add(user)
        return user
