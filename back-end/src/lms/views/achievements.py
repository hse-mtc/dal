from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from common.constants import MUTATE_ACTIONS

from auth.models import Permission
from auth.permissions import BasePermission

from lms.models.achievements import Achievement
from lms.models.students import Student
from lms.models.teachers import Teacher

from lms.serializers.achievements import (
    AchievementSerializer,
    AchievementMutateSerializer,
)

from lms.filters.achievements import AchievementFilter

from lms.utils.mixins import QuerySetScopingMixin

from lms.types.personnel import Personnel


class AchievementPermission(BasePermission):
    permission_class = "achievements"
    view_name_rus = "Достижения"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
        Permission.Scope.MILGROUP,
        Permission.Scope.SELF,
    ]


@extend_schema(tags=["achievements"])
class AchievementViewSet(QuerySetScopingMixin, ModelViewSet):
    queryset = Achievement.objects.all()

    permission_classes = [AchievementPermission]
    scoped_permission_class = AchievementPermission
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = AchievementFilter
    search_fields = ["text"]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return AchievementMutateSerializer
        return AchievementSerializer

    def handle_scope_milfaculty(self, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        return self.queryset.filter(student__milgroup__milfaculty=milfaculty)

    def allow_scope_milfaculty_on_create(self, data, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        student = Student.objects.filter(id=data["student"])
        if not student.exists():
            return False

        return milfaculty == student.first().milgroup.milfaculty

    def handle_scope_milgroup(self, personnel: Personnel):
        match personnel:
            case Student():
                milgroup = personnel.milgroup
                return self.queryset.filter(student__milgroup=milgroup)
            case Teacher():
                milgroups = personnel.milgroups
                return self.queryset.filter(student__milgroup__in=milgroups)
            case _:
                assert False, "Unhandled Personnel type"

    def allow_scope_milgroup_on_create(self, data, personnel: Personnel):
        student = Student.objects.filter(id=data["student"])
        if not student.exists():
            return False
        student = student.first()

        match personnel:
            case Student():
                return student.milgroup == personnel.milgroup
            case Teacher():
                return student.milgroup in personnel.milgroups
            case _:
                assert False, "Unhandled Personnel type"

    def handle_scope_self(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.filter(student=personnel)
            case Teacher():
                return self.queryset.none()
            case _:
                assert False, "Unhandled Personnel type"

    def allow_scope_self_on_create(self, data, personnel: Personnel):
        match personnel:
            case Student():
                return data["student"] == personnel.id
            case Teacher():
                return False
            case _:
                assert False, "Unhandled Personnel type"
