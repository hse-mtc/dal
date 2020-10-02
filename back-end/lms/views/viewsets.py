from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from lms.models import Student, Teacher
from lms.serializers.student import StudentSerializer
from lms.serializers.teacher import TeacherSerializer
from lms.filters import StudentFilterSet, TeacherFilterSet


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = StudentFilterSet
    search_fields = ['surname', 'name', 'patronymic']



class TeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = TeacherFilterSet
    search_fields = ['surname', 'name', 'patronymic']
