from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema
from common.constants import MUTATE_ACTIONS

from lms.models.punishments import Punishment
from lms.serializers.punishments import PunishmentSerializer, PunishmentMutateSerializer
from lms.filters.punishment import PunishmentFilter

from auth.permissions import BasicPermission


class PunishmentPermission(BasicPermission):
    permission_class = 'auth.punishment'


@extend_schema(tags=['punishment'])
class PunishmentViewSet(ModelViewSet):
    queryset = Punishment.objects.all()

    permission_classes = [PunishmentPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = PunishmentFilter
    search_fields = ['student__surname', 'student__name', 'student__patronymic']

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return PunishmentMutateSerializer
        return PunishmentSerializer
