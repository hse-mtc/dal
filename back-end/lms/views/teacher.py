from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from lms.models.teacher import Teacher
from lms.serializers.teacher import TeacherSerializer
from lms.filters.teacher import TeacherFilterSet


@extend_schema(tags=['teacher'])
class TeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = TeacherFilterSet
    search_fields = ['surname', 'name', 'patronymic']
