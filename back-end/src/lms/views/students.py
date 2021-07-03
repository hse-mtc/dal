import requests

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework import permissions
from rest_framework import pagination

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import BaseRenderer

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema, OpenApiParameter

from conf.settings import (
    WATCHDOC_HOST,
    WATCHDOC_PORT,
)

from common.constants import MUTATE_ACTIONS

from lms.models.applicants import ApplicationProcess
from lms.models.students import Student
from lms.models.common import (
    Milgroup,
    Milspecialty,
)

from lms.filters.students import StudentFilter

from lms.serializers.applicants import (
    ApplicantSerializer,
    ApplicationProcessSerializer,
    ApplicantWithApplicationSerializer,
)
from lms.serializers.students import (
    StudentSerializer,
    StudentMutateSerializer,
)

from lms.utils.export import generate_excel
from lms.mixins import QuerySetScopingMixin

from auth.models import Permission
from auth.serializers import CreatePasswordTokenSerializer
from auth.permissions import BasePermission


class XLSXRenderer(BaseRenderer):
    media_type = "application/xlsx"
    format = "xlsx"
    charset = None
    render_style = "binary"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class StudentPermission(BasePermission):
    permission_class = "student"
    view_name_rus = "Студенты"
    # do not allow student creation in this permission,
    # as it is handled by the applicant's form procedures
    methods = ["get", "put", "patch", "delete"]
    scopes = [
        Permission.Scopes.ALL,
        Permission.Scopes.MILFACULTY,
        Permission.Scopes.MILGROUP,
        Permission.Scopes.SELF,
    ]


class ApplicantPermission(BasePermission):
    permission_class = "applicant"
    view_name_rus = "Абитуриенты"
    methods = ["get", "post", "patch"]


class ActivatePermission(BasePermission):
    permission_class = "activate-student"
    view_name_rus = "Подтверждение регистрации"
    methods = ["get", "put", "patch"]
    scopes = [
        Permission.Scopes.ALL,
        Permission.Scopes.MILFACULTY,
        Permission.Scopes.MILGROUP,
    ]


class StudentPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"


@extend_schema(tags=["students"])
class StudentViewSet(QuerySetScopingMixin, ModelViewSet):
    # pylint: disable=too-many-public-methods
    queryset = Student.objects.order_by("surname", "name", "patronymic", "id")

    permission_classes = [StudentPermission]
    scoped_permission_class = StudentPermission

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = StudentFilter
    search_fields = ["surname", "name", "patronymic"]

    pagination_class = StudentPageNumberPagination

    def get_serializer_class(self):
        if self.action == "applications":
            return ApplicantWithApplicationSerializer
        if self.action == "application":
            return ApplicationProcessSerializer
        if self.action in MUTATE_ACTIONS:
            return StudentMutateSerializer
        return StudentSerializer

    def get_queryset(self):
        if self.action == "applications":
            return self.queryset.filter(status=Student.Status.APPLICANT)
        return super().get_queryset()

    def handle_scope_milfaculty(self, user_type, user):
        if user_type == "student":
            milfaculty = user.milgroup.milfaculty
        elif user_type == "teacher":
            milfaculty = user.milfaculty
        else:
            return self.queryset.none()
        return self.queryset.filter(milgroup__milfaculty=milfaculty)

    def handle_scope_milgroup(self, user_type, user):
        if user_type in ("student", "teacher"):
            return self.queryset.filter(milgroup=user.milgroup)
        return self.queryset.none()

    def handle_scope_self(self, user_type, user):
        if user_type == "student":
            return self.queryset.filter(user=user)
        return self.queryset.none()

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        if self.action == "applications":
            campuses = self.request.user.campuses
            queryset = queryset.filter(university_info__campus__in=campuses)

        return queryset

    def create(self, request, *args, **kwargs):
        # pylint: disable=too-many-locals

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        generate_documents = serializer.validated_data.pop("generate_documents")
        instance = self.perform_create(serializer)

        if generate_documents:
            applicant = ApplicantSerializer(instance=instance)
            response = requests.post(
                f"http://{WATCHDOC_HOST}:{WATCHDOC_PORT}/applicants/",
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

    # TODO(@gakhromov): insert required permissions in actions
    @action(detail=False,
            methods=["patch"],
            permission_classes=[permissions.AllowAny])
    def registration(self, request):
        email = request.data["email"]
        milgroup = Milgroup.objects.get(pk=request.data["milgroup"])
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

    @extend_schema(parameters=[
        OpenApiParameter(name="campus",
                         description="Filter by campus",
                         required=True,
                         type=str),
        OpenApiParameter(name="program",
                         description="Filter by program code",
                         required=False,
                         type=str),
    ])
    @action(detail=False,
            methods=["get"],
            permission_classes=[ApplicantPermission])
    def applications(self, request: Request, *args, **kwargs) -> Response:
        """List all applicants with their applications."""
        return super().list(request, *args, **kwargs)

    @action(detail=True,
            methods=["patch"],
            permission_classes=[ApplicantPermission])
    def application(self, request: Request, pk=None) -> Response:
        """Create or edit applicant's application."""

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

    @extend_schema(parameters=[
        OpenApiParameter(name="campus",
                         description="Filter by campus",
                         required=True,
                         type=str)
    ])
    @action(methods=["get"],
            url_path="applications/export",
            detail=False,
            renderer_classes=[XLSXRenderer],
            permission_classes=[ApplicantPermission])
    def applications_export(self, request: Request) -> Response:
        """
        Send an excel file with info about applicants.
        Applicants are filtered by campus, specified in request query params.
        """

        if "campus" not in request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        campus = request.query_params["campus"]
        students = self.queryset.filter(
            status=Student.Status.APPLICANT,
            university_info__campus=campus,
        )
        milspecialties = Milspecialty.objects.filter(
            available_for__contains=[campus])

        path = generate_excel(students, milspecialties)
        with open(path, "rb") as file:
            export = file.read()
        path.unlink(missing_ok=True)

        return Response(
            export,
            headers={
                "Content-Disposition": "attachment; filename=export.xlsx",
            },
            content_type="application/xlsx",
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["students"])
class ActivateStudentViewSet(QuerySetScopingMixin, ModelViewSet):
    queryset = Student.objects.all()

    permission_classes = [ActivatePermission]
    scoped_permission_class = ActivatePermission

    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
    serializer_class = StudentSerializer

    def handle_scope_milfaculty(self, user_type, user):
        if user_type == "student":
            milfaculty = user.milgroup.milfaculty
        elif user_type == "teacher":
            milfaculty = user.milfaculty
        else:
            return self.queryset.none()
        return self.queryset.filter(milgroup__milfaculty=milfaculty)

    def handle_scope_milgroup(self, user_type, user):
        if user_type in ("student", "teacher"):
            return self.queryset.filter(milgroup=user.milgroup)
        return self.queryset.none()

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset().filter(status__in=[
            Student.Status.APPLICANT,
            Student.Status.DECLINED,
            Student.Status.AWAITING,
        ])

        user = request.user
        milgroup = None

        if hasattr(user, "teacher"):
            milgroup = user.teacher.milgroup
        elif hasattr(user, "student"):
            milgroup = user.student.milgroup

        if milgroup is not None:
            queryset = queryset.filter(milgroup=milgroup)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        return serializer.save()

    def update(self, request: Request, *args, **kwargs) -> Response:
        partial = kwargs.pop("partial", False)
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
            print(f"localhost:9528/change-password?token={str(token)}")

        if getattr(instance, "_prefetched_objects_cache", None):
            # If "prefetch_related" has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            # pylint: disable=protected-access
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
