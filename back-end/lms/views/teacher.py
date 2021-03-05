from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from lms.models.teachers import Teacher
from lms.serializers.teachers import TeacherSerializer
from lms.filters.teacher import TeacherFilter

from auth.permissions import BasicPermission


class TeacherPermission(BasicPermission):
    permission_class = 'auth.teacher'


@extend_schema(tags=['teacher'])
class TeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    permission_classes = [TeacherPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = TeacherFilter
    search_fields = ['surname', 'name', 'patronymic']
