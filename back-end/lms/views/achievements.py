from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema
from common.constants import MUTATE_ACTIONS

from lms.models.achievements import Achievement
from lms.serializers.achievements import AchievementSerializer, AchievementMutateSerializer
from lms.filters.achievement import AchievementFilter

from auth.permissions import BasicPermission


class AchievementPermission(BasicPermission):
    permission_class = 'auth.achievement'


@extend_schema(tags=['achievements'])
class AchievementViewSet(ModelViewSet):
    queryset = Achievement.objects.all()

    permission_classes = [AchievementPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = AchievementFilter
    search_fields = ['text']

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return AchievementMutateSerializer
        return AchievementSerializer
