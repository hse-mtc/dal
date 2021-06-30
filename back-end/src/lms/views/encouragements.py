from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema
from common.constants import MUTATE_ACTIONS

from lms.models.students import Student
from lms.models.teachers import Teacher
from lms.models.encouragements import Encouragement
from lms.serializers.encouragements import (EncouragementSerializer,
                                            EncouragementMutateSerializer)
from lms.filters.encouragements import EncouragementFilter

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
class EncouragementViewSet(ModelViewSet):
    queryset = Encouragement.objects.all()

    permission_classes = [EncouragementPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = EncouragementFilter
    search_fields = ['student__surname', 'student__name', 'student__patronymic']

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return EncouragementMutateSerializer
        return EncouragementSerializer

    # pylint: disable=too-many-return-statements
    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset

        scope = self.request.user.get_perm_scope(
            EncouragementPermission.permission_class, self.request.method)

        if scope == Permission.Scopes.ALL:
            return self.queryset

        # check if user is a teacher ot a student
        user = Teacher.objects.filter(user=self.request.user)
        user_type = 'teacher'
        if user.count() == 0:
            # check if user is a student
            user = Student.objects.filter(user=self.request.user)
            user_type = 'student'
            if user.count() == 0:
                # return nothing is user is not a student or a teacher
                return self.queryset.none()

        if scope == Permission.Scopes.SELF:
            res = self.queryset.filter(**{user_type: user[0]})
            if res.count() == 0:
                return self.queryset.none()
            return res

        if scope == Permission.Scopes.MILGROUP:
            # we are only interested in encouragements that
            # are given to students of milgroup == teacher/student milgroup
            res = self.queryset.filter(student__milgroup=user[0].milgroup)
            if res.count() == 0:
                return self.queryset.none()
            return res

        if scope == Permission.Scopes.MILFACULTY:
            # we are only interested in encouragements that
            # are given to students of milfaculty == teacher/student milfaculty
            res = self.queryset.filter(
                student__milgroup__milfaculty=user[0].milfaculty)
            if res.count() == 0:
                return self.queryset.none()
            return res

        return self.queryset.none()
