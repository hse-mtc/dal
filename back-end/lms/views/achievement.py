from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from lms.models.achievement import Achievement
from lms.serializers.achievement import AchievementSerializer
from lms.filters.achievement import AchievementFilter


@extend_schema(tags=['achievement'])
class AchievementViewSet(ModelViewSet):
    serializer_class = AchievementSerializer
    queryset = Achievement.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = AchievementFilter
    search_fields = ['text']
