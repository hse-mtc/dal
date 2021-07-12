from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema
from common.constants import MUTATE_ACTIONS

from lms.models.achievements import Achievement
from lms.models.students import Student
from lms.serializers.achievements import (AchievementSerializer,
                                          AchievementMutateSerializer)
from lms.filters.achievements import AchievementFilter
from lms.mixins import QuerySetScopingMixin

from auth.models import Permission
from auth.permissions import BasePermission


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

    def handle_scope_milfaculty(self, user_type, user):
        if user_type == "student":
            milfaculty = user.milgroup.milfaculty
        if user_type == "teacher":
            milfaculty = user.milfaculty
        else:
            return self.queryset.none()
        return self.queryset.filter(student__milgroup__milfaculty=milfaculty)

    def allow_scope_milfaculty_on_create(self, data, user_type, user):
        if user_type == "student":
            milfaculty = user.milgroup.milfaculty
        if user_type == "teacher":
            milfaculty = user.milfaculty
        else:
            return False

        student = Student.objects.filter(id=data["student"])
        if not student.exists():
            return False

        return milfaculty == student.first().milgroup.milfaculty

    def handle_scope_milgroup(self, user_type, user):
        if user_type == "student":
            milgroup = user.milgroup
            return self.queryset.filter(student__milgroup=milgroup)

        if user_type == "teacher":
            milgroups = user.milgroups
            return self.queryset.filter(student__milgroup__in=milgroups)

        return self.queryset.none()

    def allow_scope_milgroup_on_create(self, data, user_type, user):
        student = Student.objects.filter(id=data["student"])
        if not student.exists():
            return False
        student = student.first()

        if user_type == "student":
            return student.milgroup == user.milgroup

        if user_type == "teacher":
            return student.milgroup in user.milgroups

        return False

    def handle_scope_self(self, user_type, user):
        if user_type == "student":
            return self.queryset.filter(student=user)
        return self.queryset.none()

    def allow_scope_self_on_create(self, data, user_type, user):
        if user_type == "student":
            return data["student"] == user.id
        return False
