from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from lms.models.lesson import Lesson
from lms.serializers.lesson import LessonSerializer
from lms.filters.lesson import LessonFilter


@extend_schema(tags=['lesson'])
class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]

    filterset_class = LessonFilter
