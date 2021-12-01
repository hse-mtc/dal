import requests

from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from conf import settings

from common.constants import MUTATE_ACTIONS

from auth.models import Permission
from auth.permissions import BasePermission

from lms.models.students import Student
from lms.models.teachers import Teacher
from lms.models.uniforms import Uniform

from lms.serializers.uniforms import (
    UniformSerializer,
    UniformMutateSerializer,
)

from lms.filters.uniforms import UniformFilter

from lms.utils.mixins import QuerySetScopingMixin

from lms.types.personnel import Personnel


class UniformPermission(BasePermission):
    permission_class = "uniforms"
    view_name_rus = "Форма одежды"
    methods = ["get", "patch"]
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
    ]


@extend_schema(tags=["uniforms"])
class UniformViewSet(QuerySetScopingMixin, ModelViewSet):
    queryset = Uniform.objects.all()

    permission_classes = [UniformPermission]
    scoped_permission_class = UniformPermission
    filter_backends = [DjangoFilterBackend]

    filterset_class = UniformFilter

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return UniformMutateSerializer
        return UniformSerializer

    def perform_update(self, serializer: UniformSerializer):
        serializer.save()
        requests.post(
            f"http://{settings.TGBOT_HOST}:{settings.TGBOT_PORT}/uniforms/",
            data=JSONRenderer().render(serializer.data),
        )

    def handle_scope_milfaculty(self, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        return self.queryset.filter(milfaculty=milfaculty)

    def allow_scope_milfaculty_on_create(self, data, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        return data["milfaculty"] == milfaculty.id
