import requests

from rest_framework import status
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
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


@extend_schema(tags=['activate-students'])
class ActivateStudentReadonlyViewSet(ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    permission_classes = [StudentPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
    serializer_class = StudentSerializer

    def get_queryset(self):
        user = self.request.user
        is_teacher = hasattr(user, 'teacher')
        is_student = hasattr(user, 'student')

        milgroup = None

        if is_teacher:
            milgroup = user.teacher.milgroup
        elif is_student:
            milgroup = user.student.milgroup

        return Student.objects.filter(milgroup=milgroup)

    def set_status(self, status):
        student = self.get_object()
        student.status = status
        student.save()

        serializer = self.get_serializer(student)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        return self.set_status(Student.Status.STUDENT.value)

    @action(detail=True, methods=['post'])
    def wait(self, request, pk=None):
        return self.set_status(Student.Status.AWAITING.value)

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        return self.set_status(Student.Status.DECLINED.value)


