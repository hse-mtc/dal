from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from lms.models import Student, Teacher, Punishment, Encouragement
from lms.serializers.student import StudentSerializer
from lms.serializers.teacher import TeacherSerializer
from lms.serializers.punishment import PunishmentSerializer
from lms.serializers.encouragement import EncouragementSerializer
from lms.filters import (StudentFilterSet, TeacherFilterSet,
                         PunishmentFilterSet, EncouragementFilterSet)


@extend_schema(tags=['student'])
class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = StudentFilterSet
    search_fields = ['surname', 'name', 'patronymic']


@extend_schema(tags=['teacher'])
class TeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = TeacherFilterSet
    search_fields = ['surname', 'name', 'patronymic']


@extend_schema(tags=['punishment'])
class PunishmentViewSet(ModelViewSet):
    serializer_class = PunishmentSerializer
    queryset = Punishment.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = PunishmentFilterSet
    search_fields = ['student__surname', 'student__name', 'student__patronymic']


@extend_schema(tags=['encouragement'])
class EncouragementViewSet(ModelViewSet):
    serializer_class = EncouragementSerializer
    queryset = Encouragement.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = EncouragementFilterSet
    search_fields = ['student__surname', 'student__name', 'student__patronymic']
