from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema
from common.constants import MUTATE_ACTIONS

from lms.models.teachers import Teacher
from lms.serializers.teachers import TeacherSerializer, TeacherMutateSerializer
from lms.filters.teachers import TeacherFilter
from lms.mixins import QuerySetScopingMixin

from auth.models import Permission
from auth.permissions import BasePermission


class TeacherPermission(BasePermission):
    permission_class = "teacher"
    view_name_rus = "Учителя"
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
        if self.action in MUTATE_ACTIONS:
            return TeacherMutateSerializer
        return TeacherSerializer

    def handle_scope_milfaculty(self, user_type, user):
        if user_type == "student":
            milfaculty = user.milgroup.milfaculty
        elif user_type == "teacher":
            milfaculty = user.milfaculty
        else:
            return self.queryset.none()
        return self.queryset.filter(milfaculty=milfaculty)

    def allow_scope_milfaculty_on_create(self, data, user_type, user):
        if user_type == "student":
            milfaculty = user.milgroup.milfaculty
        elif user_type == "teacher":
            milfaculty = user.milfaculty
        else:
            return False
        return data["milfaculty"] == milfaculty.milfaculty

    def handle_scope_self(self, user_type, user):
        if user_type == "teacher":
            return self.queryset.filter(user=self.request.user)
        return self.queryset.none()

    def allow_scope_self_on_create(self, data, user_type, user):
        if user_type == "teacher":
            return data["user"] == user.id
        return False
