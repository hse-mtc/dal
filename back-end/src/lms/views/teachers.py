from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema
from common.constants import MUTATE_ACTIONS

from lms.models.teachers import Teacher
from lms.serializers.teachers import TeacherSerializer, TeacherMutateSerializer
from lms.filters.teachers import TeacherFilter

from auth.permissions import BasePermission


class TeacherPermission(BasePermission):
    permission_class = 'teacher'


@extend_schema(tags=['teachers'])
class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()

    permission_classes = [TeacherPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = TeacherFilter
    search_fields = ['surname', 'name', 'patronymic']

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return TeacherMutateSerializer
        return TeacherSerializer
