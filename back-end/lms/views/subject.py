from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from common.models.subjects import Subject

from lms.serializers.subject import LessonSubjectSerializer
from lms.filters.subject import LessonSubjectFilter


@extend_schema(tags=['lms_subject'])
class LessonSubjectViewSet(ModelViewSet):
    serializer_class = LessonSubjectSerializer
    queryset = Subject.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = LessonSubjectFilter
    search_fields = [
        'title',
    ]
