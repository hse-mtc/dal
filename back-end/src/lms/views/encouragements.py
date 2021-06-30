from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema
from common.constants import MUTATE_ACTIONS

from lms.models.encouragements import Encouragement
from lms.serializers.encouragements import (EncouragementSerializer,
                                            EncouragementMutateSerializer)
from lms.filters.encouragements import EncouragementFilter
from lms.views.views import BasicQuerysetScoping

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
class EncouragementViewSet(BasicQuerysetScoping, ModelViewSet):
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
        if res.count() == 0:
            return self.queryset.none()
        return res

    def handle_scope_milgroup(self, user_type, user):
        # we are only interested in encouragements that
        # are given to students of milgroup == teacher/student milgroup
        res = self.queryset.filter(student__milgroup=user.milgroup)
        if res.count() == 0:
            return self.queryset.none()
        return res

    def handle_scope_self(self, user_type, user):
        res = self.queryset.filter(**{user_type: user})
        if res.count() == 0:
            return self.queryset.none()
        return res
