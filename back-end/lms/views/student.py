from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from lms.models.student import Student
from lms.serializers.student import StudentSerializer
from lms.filters.student import StudentFilterSet


@extend_schema(tags=['student'])
class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = StudentFilterSet
    search_fields = ['surname', 'name', 'patronymic']
