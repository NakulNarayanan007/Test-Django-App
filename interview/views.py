from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from interview.models import Schedule
from interview.serializers import (ListScheduleSerializer,
                                   ScheduleModelSerializer)


class RegisterScheduleView(CreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleModelSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class GetScheduleView(GenericAPIView):
    serializer_class = ListScheduleSerializer
    queryset = Schedule.objects.all()
    # permission_classes = (IsAdminUser, )

    def post(self, request, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.time_slots, status=status.HTTP_200_OK)
