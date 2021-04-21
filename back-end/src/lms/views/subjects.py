from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from common.models.subjects import Subject

from lms.serializers.subjects import LessonSubjectSerializer
from lms.filters.subjects import LessonSubjectFilter

from auth.permissions import BasePermission


class LessonSubjectPermission(BasePermission):
    permission_class = 'auth.subject'


@extend_schema(tags=['lms-subjects'])
class LessonSubjectViewSet(ModelViewSet):
    serializer_class = LessonSubjectSerializer
    queryset = Subject.objects.all()

    permission_classes = [LessonSubjectPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = LessonSubjectFilter
    search_fields = [
        'title',
    ]
