import requests

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from conf.settings import (
    WATCHDOC_HOST,
    WATCHDOC_PORT,
)

from common.constants import MUTATE_ACTIONS

from lms.models.common import Milgroup
from lms.models.applicants import ApplicationProcess
from lms.models.students import Student

from lms.filters.students import StudentFilter

from lms.serializers.applicants import (
    ApplicantSerializer,
    ApplicationProcessSerializer,
)
from lms.serializers.students import (
    StudentSerializer,
    StudentMutateSerializer,
)

from auth.serializers import CreatePasswordTokenSerializer
from auth.permissions import BasePermission


class StudentPermission(BasePermission):
    permission_class = 'auth.student'


class AllowStudentPost(permissions.BasePermission):

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
        if self.action == 'application':
            return ApplicationProcessSerializer
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

    @action(detail=False, methods=['patch'])
    def registration(self, request):
        email = request.data['email']
        milgroup = Milgroup.objects.get(pk=request.data['milgroup'])
        user = get_user_model().objects.create_user(
            email=email,
            password=get_user_model().objects.make_random_password(),
        )

        instance = Student.objects.filter(
            contact_info__corporate_email=email).first()
        instance.milgroup = milgroup
        instance.user = user
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def application(self, request: Request, pk=None) -> Response:
        # pylint: disable=unused-argument,invalid-name

        serializer = ApplicationProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = self.get_object()
        if not student.application_process:
            student.application_process = ApplicationProcess.objects.create()

        updated = serializer.update(
            instance=student.application_process,
            validated_data=serializer.validated_data,
        )
        student.application_process = updated
        student.save()

        return Response(
            status=status.HTTP_200_OK,
            data=ApplicationProcessSerializer(instance=updated).data,
        )


@extend_schema(tags=['students'])
class ActivateStudentViewSet(ModelViewSet):
    queryset = Student.objects.all()

    permission_classes = [StudentPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
    serializer_class = StudentSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset().filter(status__in=[
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

    def perform_update(self, serializer):
        return serializer.save()

    def update(self, request: Request, *args, **kwargs) -> Response:
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        instance: Student = self.perform_update(serializer)

        if instance.status == Student.Status.STUDENT:
            email = instance.contact_info.corporate_email
            user = get_user_model().objects.get(email=email)
            token = CreatePasswordTokenSerializer.get_token(user)

            # TODO(TmLev): send email, link should forward to front end app
            print(f'localhost:9528/change-password?token={str(token)}')

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            # pylint: disable=protected-access
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
