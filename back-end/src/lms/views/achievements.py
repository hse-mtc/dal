from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema
from common.constants import MUTATE_ACTIONS

from lms.models.achievements import Achievement
from lms.serializers.achievements import (AchievementSerializer,
                                          AchievementMutateSerializer)
from lms.filters.achievements import AchievementFilter
from lms.views.archived_viewset import ArchivedModelViewSet

from auth.permissions import BasePermission


class AchievementPermission(BasePermission):
    permission_class = 'auth.achievement'


@extend_schema(tags=['achievements'])
class AchievementViewSet(ArchivedModelViewSet):
    queryset = Achievement.objects.all()

    permission_classes = [AchievementPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = AchievementFilter
    search_fields = ['text']

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return AchievementMutateSerializer
        return AchievementSerializer
