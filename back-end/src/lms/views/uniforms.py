import requests

from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer
from drf_spectacular.views import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from lms.models.uniforms import Uniform
from lms.serializers.uniforms import UniformSerializer, UniformMutateSerializer
from lms.filters.uniforms import UniformFilter
from lms.mixins import QuerySetScopingMixin

from conf.settings import (
    TGBOT_PORT,
    TGBOT_HOST,
)
from common.constants import MUTATE_ACTIONS
from auth.models import Permission
from auth.permissions import BasePermission


class UniformPermission(BasePermission):
    permission_class = 'uniform'
    view_name_rus = 'Форма одежды'
    scopes = [
        Permission.Scopes.ALL,
        Permission.Scopes.MILFACULTY,
    ]


@extend_schema(tags=['uniforms'])
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
            f'http://{TGBOT_HOST}:{TGBOT_PORT}/uniforms/',
            data=JSONRenderer().render(serializer.data),
        )

    def handle_scope_milfaculty(self, user_type, user):
        if user_type == 'student':
            milfaculty = user.milgroup.milfaculty
        elif user_type == 'teacher':
            milfaculty = user.milfaculty
        else:
            return self.queryset.none()
        return self.queryset.filter(milfaculty=milfaculty)

    def allow_scope_milfaculty_on_create(self, data, user_type, user):
        if user_type == 'student':
            return data['milfaculty'] == user.milgroup.milfaculty.milfaculty
        if user_type == 'teacher':
            return data['milfaculty'] == user.milfaculty.milfaculty
        return False
