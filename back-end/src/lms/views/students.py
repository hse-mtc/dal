import requests

from rest_framework import status

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import BasePermission
from rest_framework.renderers import JSONRenderer

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from conf.settings import (
    WATCHDOC_HOST,
    WATCHDOC_PORT,
)

from common.constants import MUTATE_ACTIONS

from lms.models.students import Student
from lms.filters.students import StudentFilter
from lms.serializers.students import (
    StudentSerializer,
    StudentMutateSerializer,
    ApplicantSerializer,
)

from auth.permissions import BasicPermission


class StudentPermission(BasicPermission):
    permission_class = 'auth.student'


class AllowStudentPost(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method == 'POST'


@extend_schema(tags=['students'])
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()

    permission_classes = [AllowStudentPost | StudentPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = StudentFilter
    search_fields = ['surname', 'name', 'patronymic']

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return StudentMutateSerializer
        return StudentSerializer

    def create(self, request, *args, **kwargs):
        # pylint: disable=too-many-locals

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        applicant = ApplicantSerializer(instance=instance)
        requests.post(
            f'http://{WATCHDOC_HOST}:{WATCHDOC_PORT}/applicants/',
            data=JSONRenderer().render(applicant.data),
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
