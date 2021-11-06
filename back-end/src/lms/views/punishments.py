from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from common.constants import MUTATE_ACTIONS

from common.views.choices import GenericChoicesList

from auth.models import Permission
from auth.permissions import BasePermission

from lms.models.punishments import Punishment

from lms.serializers.punishments import (
    PunishmentSerializer,
    PunishmentMutateSerializer,
)

from lms.filters.punishments import PunishmentFilter

from lms.utils.mixins import StudentTeacherQuerySetScopingMixin


class PunishmentPermission(BasePermission):
    permission_class = "punishments"
    view_name_rus = "Взыскания"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
        Permission.Scope.MILGROUP,
        Permission.Scope.SELF,
    ]


@extend_schema(tags=["punishments"])
class PunishmentViewSet(StudentTeacherQuerySetScopingMixin, ModelViewSet):
    queryset = Punishment.objects.all()

    permission_classes = [PunishmentPermission]
    scoped_permission_class = PunishmentPermission

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = PunishmentFilter
    search_fields = ["student__surname", "student__name", "student__patronymic"]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return PunishmentMutateSerializer
        return PunishmentSerializer


@extend_schema(tags=["punishments", "choices"])
class PunishmentTypeChoicesList(GenericChoicesList):
    choices_class = Punishment.Type
