from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from lms.models import Student, Teacher, Punishment
from lms.serializers.student import StudentSerializer
from lms.serializers.teacher import TeacherSerializer
from lms.serializers.punishment import PunishmentSerializer
from lms.filters import StudentFilterSet, TeacherFilterSet, PunishmentFilterSet


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


class PunishmentViewSet(ModelViewSet):
    serializer_class = PunishmentSerializer
    queryset = Punishment.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = PunishmentFilterSet
    search_fields = ['student__surname', 'student__name', 'student__patronymic']
