from rest_framework import permissions

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import get_user_model

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from common.constants import MUTATE_ACTIONS

from common.views.choices import GenericChoicesList

from auth.models import Permission
from auth.permissions import BasePermission

from lms.models.students import Student
from lms.models.teachers import Teacher

from lms.serializers.teachers import (
    TeacherSerializer,
    TeacherMutateSerializer,
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
class TeacherViewSet(QuerySetScopingMixin, ModelViewSet):
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

    @action(detail=False,
            methods=["post"],
            permission_classes=[permissions.AllowAny])
    def registration(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher = self.perform_create(serializer)

        # NB: Email uniqueness is guaranteed by ContactInfo.email field.
        email = serializer.validated_data["contact_info"]["corporate_email"]
        user = get_user_model().objects.create_user(
            email=email,
            password=get_user_model().objects.make_random_password(),
            campuses=["MO"],
        )
        teacher.user = user
        teacher.save()

        # TODO(TmLev): Send confirmation email with link to set password.

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


@extend_schema(tags=["teachers", "choices"])
class TeacherRankChoicesList(GenericChoicesList):
    choices_class = Teacher.Rank


@extend_schema(tags=["teachers", "choices"])
class TeacherPostChoicesList(GenericChoicesList):
    choices_class = Teacher.Post
