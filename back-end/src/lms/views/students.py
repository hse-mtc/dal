import requests

from rest_framework import status

from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import BasePermission
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from conf.settings import (
    WATCHDOC_HOST,
    WATCHDOC_PORT,
)

from common.constants import MUTATE_ACTIONS

from lms.models.students import Student
from lms.filters.students import StudentFilter
from lms.serializers.applicants import ApplicantSerializer
from lms.serializers.students import (
    StudentSerializer,
    StudentMutateSerializer,
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
        instance: Student = self.perform_create(serializer)

        if instance.status == Student.Status.APPLICANT:
            applicant = ApplicantSerializer(instance=instance)
            response = requests.post(
                f'http://{WATCHDOC_HOST}:{WATCHDOC_PORT}/applicants/',
                data=JSONRenderer().render(applicant.data),
            )
            # TODO(TmLev): remove debug print
            print(response.json())

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


@extend_schema(tags=['students'])
class ActivateStudentViewSet(ModelViewSet):
    queryset = Student.objects.all()

    permission_classes = [StudentPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
    serializer_class = StudentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(
            status__in=[
                Student.Status.APPLICANT,
                Student.Status.DECLINED,
                Student.Status.AWAITING,
            ])

        user = request.user
        milgroup = None

        if hasattr(user, 'teacher'):
            milgroup = user.teacher.milgroup
        elif hasattr(user, 'student'):
            milgroup = user.student.milgroup

        if milgroup is not None:
            queryset = queryset.filter(milgroup=milgroup)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
