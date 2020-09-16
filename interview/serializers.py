from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers

from interview.models import Schedule
from utils import generate_time_slots, rounder


class ScheduleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        exclude = [
            "user",
        ]

    def create(self, validated_data):
        obj = self.Meta.model(**validated_data)
        obj.user = self.context["request"].user
        obj.save()
        return obj

    def validate(self, attrs):
        errors = dict()
        # validate date start should be less than date end:

        if attrs.get("available_time_slot_start") > attrs.get(
            "available_time_slot_end"
        ):
            errors[
                "available_time_slot_start"
            ] = "Start time should be less than end Time"
            errors[
                "available_time_slot_end"
            ] = "End time should be greater than Start Time"
        # validate minimum time duration
        time_delta = attrs.get("available_time_slot_end") - attrs.get(
            "available_time_slot_start"
        )
        if time_delta.total_seconds() < 60 * 60:
            errors["non_field_errors"] = "Time Duration should be minimum 1 hour"
        return attrs


class ListScheduleSerializer(serializers.Serializer):

    candidate_id = serializers.IntegerField()
    interviewer_id = serializers.IntegerField()

    def validate_candidate_id(self, attr):
        qs = User.objects.filter(groups__name=settings.CANDIDATE_GROUP_NAME, id=attr)
        if not qs:
            raise serializers.ValidationError("Invalid candidate ID")

        return attr

    def validate_interviewer_id(self, attr):
        qs = User.objects.filter(groups__name=settings.INTERVIEWER_GROUP_NAME, id=attr)
        if not qs:
            raise serializers.ValidationError("Invalid Interviewer  ID")
        return attr

    def validate(self, attrs):
        """
        Validate the schedule checking whether if there is a overlapping time slots or is there any time timeslots
        """
        errors = dict()
        # validate candidate schedule
        cs_qs = Schedule.objects.filter(user__id=attrs.get("candidate_id"))
        if not cs_qs:
            errors[
                "candidate_id"
            ] = f"No Schedule Found for candidate id {attrs.get('candidate_id')}"

        # validate interviewer schedule
        is_qs = Schedule.objects.filter(user__id=attrs.get("interviewer_id"))
        if not cs_qs:
            errors[
                "interviewer_id"
            ] = f"No Schedule Found for interviewer id {attrs.get('candidate_id')}"

        # validate both have common dates
        time_slots = []
        if cs_qs and is_qs:
            for schedule in is_qs:
                qs = cs_qs.filter(
                    available_time_slot_start__lte=schedule.available_time_slot_start,
                    available_time_slot_end__gte=schedule.available_time_slot_end,
                )
                if qs:
                    candidate_time_slot = qs.first()
                    interviewer_time_slot = schedule
                    candidate_slots = generate_time_slots(
                        rounder(candidate_time_slot.available_time_slot_start),
                        rounder(candidate_time_slot.available_time_slot_end),
                        settings.TIME_SLOT_INTERVAL,
                    )
                    interviewer_slots = generate_time_slots(
                        rounder(interviewer_time_slot.available_time_slot_start),
                        rounder(interviewer_time_slot.available_time_slot_end),
                        settings.TIME_SLOT_INTERVAL,
                    )
                    common_timeslots = set(interviewer_slots).intersection(
                        set(candidate_slots)
                    )
                    if common_timeslots:
                        time_slots.append(
                            {
                                str(
                                    interviewer_time_slot.available_time_slot_start.date()
                                ): common_timeslots
                            }
                        )
        if time_slots:
            self.time_slots = time_slots
        else:
            errors["non_field_errors"] = "no common timeslot found"

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
