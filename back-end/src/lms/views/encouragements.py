from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema
from common.constants import MUTATE_ACTIONS

from lms.models.encouragements import Encouragement
from lms.serializers.encouragements import (EncouragementSerializer,
                                            EncouragementMutateSerializer)
from lms.filters.encouragements import EncouragementFilter

from auth.permissions import BasePermission


class EncouragementPermission(BasePermission):
    permission_class = 'auth.encouragement'


@extend_schema(tags=['encouragements'])
class EncouragementViewSet(ModelViewSet):
    queryset = Encouragement.objects.all()

    permission_classes = [EncouragementPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = EncouragementFilter
    search_fields = ['student__surname', 'student__name', 'student__patronymic']

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return EncouragementMutateSerializer
        return EncouragementSerializer
