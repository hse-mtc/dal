from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from lms.models.punishment import Punishment
from lms.serializers.punishment import PunishmentSerializer
from lms.filters.punishment import PunishmentFilterSet


@extend_schema(tags=['punishment'])
class PunishmentViewSet(ModelViewSet):
    serializer_class = PunishmentSerializer
    queryset = Punishment.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = PunishmentFilterSet
    search_fields = ['student__surname', 'student__name', 'student__patronymic']
