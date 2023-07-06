from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins

from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import get_user_model

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from common.constants import MUTATE_ACTIONS
from common.email.registration import send_regconf_email
from common.views.choices import GenericChoicesList
from common.serializers.personal import check_email_exists

from auth.models import Permission
from auth.permissions import BasePermission
from auth.tokens.registration import generate_regconf_token

from lms.models.students import Student
from lms.models.teachers import Teacher

from lms.serializers.teachers import (
    TeacherSerializer,
    TeacherMutateSerializer,
    ApproveTeacherSerializer,
    ApproveTeacherMutateSerializer,
)

from lms.filters.teachers import TeacherFilter

from lms.utils.mixins import QuerySetScopingMixin

from lms.types.personnel import Personnel


class TeacherPermission(BasePermission):
    permission_class = "teachers"
    view_name_rus = "Преподаватель"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
        Permission.Scope.SELF,
    ]


@extend_schema(tags=["teachers"])
class TeacherViewSet(QuerySetScopingMixin, viewsets.ModelViewSet):
    queryset = Teacher.objects.all()

    permission_classes = [TeacherPermission]
    scoped_permission_class = TeacherPermission

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = TeacherFilter
    search_fields = ["surname", "name", "patronymic"]

    def get_serializer_class(self):
        mutate_actions = MUTATE_ACTIONS + ["registration"]
        if self.action in mutate_actions:
            return TeacherMutateSerializer
        return TeacherSerializer

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def registration(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        # NB: Email uniqueness is guaranteed by ContactInfo.email field.
        email = serializer.validated_data["contact_info"]["corporate_email"]

        if check_email_exists(email):
            return Response(
                {"error_message": "email_already_exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_user_model().objects.create_user(
            email=email,
            password=get_user_model().objects.make_random_password(),
            campuses=["MO"],
            is_active=False,
        )

        teacher = self.perform_create(serializer)
        teacher.user = user
        teacher.save()

        return Response(self.get_serializer(teacher).data)

    def perform_create(self, serializer) -> Teacher:
        return serializer.save()

    def handle_scope_milfaculty(self, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        return self.queryset.filter(milfaculty=milfaculty)

    def allow_scope_milfaculty_on_create(self, data, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        return data["milfaculty"] == milfaculty.id

    def handle_scope_self(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.none()
            case Teacher():
                return self.queryset.filter(user=personnel.user)
            case _:
                assert False, "Unhandled Personnel type"

    def allow_scope_self_on_create(self, data, personnel: Personnel):
        match personnel:
            case Student():
                return False
            case Teacher():
                return data["user"] == personnel.user.id
            case _:
                assert False, "Unhandled Personnel type"


class ApproveTeacherPermission(BasePermission):
    permission_class = "approve-teacher"
    view_name_rus = "Подтверждение регистрации преподавателей"
    methods = ["get", "patch"]
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
    ]


@extend_schema(tags=["teachers"])
class ApproveTeacherViewSet(
    QuerySetScopingMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Teacher.objects.filter(
        user__isnull=False,
        user__is_active=False,
    )

    permission_classes = [ApproveTeacherPermission]
    scoped_permission_class = ApproveTeacherPermission

    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return ApproveTeacherMutateSerializer
        return ApproveTeacherSerializer

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        teacher = self.get_object()
        serializer = self.get_serializer(teacher, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(teacher, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            teacher._prefetched_objects_cache = {}

        if teacher.patronymic:
            address = f"{teacher.name} {teacher.patronymic}"
        else:
            address = f"{teacher.name} {teacher.surname}"

        send_regconf_email(
            address=address,
            email=teacher.user.email,
            url=request.META["HTTP_REFERER"],
            token=generate_regconf_token(teacher.user),
        )

        return Response()

    def perform_update(self, serializer):
        serializer.save()

    def handle_scope_milfaculty(self, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                return self.queryset.filter(milfaculty=personnel.milfaculty)
            case _:
                assert False, "Unhandled Personnel type"


@extend_schema(tags=["teachers", "choices"])
class TeacherRankChoicesList(GenericChoicesList):
    choices_class = Teacher.Rank


@extend_schema(tags=["teachers", "choices"])
class TeacherPostChoicesList(GenericChoicesList):
    choices_class = Teacher.Post
