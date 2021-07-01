from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema
from common.constants import MUTATE_ACTIONS

from lms.models.encouragements import Encouragement
from lms.models.students import Student
from lms.serializers.encouragements import (EncouragementSerializer,
                                            EncouragementMutateSerializer)
from lms.filters.encouragements import EncouragementFilter
from lms.mixins import QuerysetScopingMixin

from auth.models import Permission
from auth.permissions import BasePermission


class EncouragementPermission(BasePermission):
    permission_class = 'encouragement'
    view_name_rus = 'Поощрения'
    scopes = [
        Permission.Scopes.ALL,
        Permission.Scopes.MILFACULTY,
        Permission.Scopes.MILGROUP,
        Permission.Scopes.SELF,
    ]


@extend_schema(tags=['encouragements'])
class EncouragementViewSet(QuerysetScopingMixin, ModelViewSet):
    queryset = Encouragement.objects.all()

    permission_classes = [EncouragementPermission]
    scoped_permission_class = EncouragementPermission

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = EncouragementFilter
    search_fields = ['student__surname', 'student__name', 'student__patronymic']

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return EncouragementMutateSerializer
        return EncouragementSerializer

    def handle_scope_milfaculty(self, user_type, user):
        # we are only interested in encouragements that
        # are given to students of milfaculty == teacher/student milfaculty
        res = self.queryset.filter(
            student__milgroup__milfaculty=user.milfaculty)
        return res

    def allow_scope_milfaculty_on_create(self, data, user_type, user):
        student = Student.objects.filter(id=data['student'])
        if student.count() == 0:
            return False
        if user_type == 'student':
            return user.milgroup.milfaculty.milfaculty == student[
                0].milgroup.milfaculty.milfaculty
        if user_type == 'teacher':
            return user.milfaculty.milfaculty == student[
                0].milgroup.milfaculty.milfaculty
        return False

    def handle_scope_milgroup(self, user_type, user):
        # we are only interested in encouragements that
        # are given to students of milgroup == teacher/student milgroup
        res = self.queryset.filter(student__milgroup=user.milgroup)
        return res

    def allow_scope_milgroup_on_create(self, data, user_type, user):
        student = Student.objects.filter(id=data['student'])
        if student.count() == 0:
            return False
        if user_type in ('student', 'teacher'):
            return user.milgroup.milgroup == student[0].milgroup.milgroup
        return False

    def handle_scope_self(self, user_type, user):
        res = self.queryset.filter(**{user_type: user})
        return res

    def allow_scope_self_on_create(self, data, user_type, user):
        if user_type == 'student':
            return data['student'] == user.id
        if user_type == 'teacher':
            return data['teacher'] == user.id
        return False
