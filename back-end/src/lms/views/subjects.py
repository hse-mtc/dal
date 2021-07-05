from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from common.models.subjects import Subject

from lms.serializers.subjects import LessonSubjectSerializer
from lms.filters.subjects import LessonSubjectFilter

from auth.models import Permission
from auth.permissions import BasePermission


class LessonSubjectPermission(BasePermission):
    permission_class = 'subject'
    view_name_rus = 'Занятия в расписании'
    methods = ['get']


@extend_schema(tags=['lms-subjects'])
class LessonSubjectViewSet(ReadOnlyModelViewSet):
    serializer_class = LessonSubjectSerializer
    queryset = Subject.objects.all()

    permission_classes = [LessonSubjectPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = LessonSubjectFilter
    search_fields = [
        'title',
    ]
