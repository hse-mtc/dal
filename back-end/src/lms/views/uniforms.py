import requests

from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer
from drf_spectacular.views import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from lms.models.uniforms import Uniform
from lms.serializers.uniforms import UniformSerializer, UniformMutateSerializer
from lms.filters.uniforms import UniformFilter

from conf.settings import (
    TGBOT_PORT,
    TGBOT_HOST,
)
from common.constants import MUTATE_ACTIONS
from auth.permissions import BasePermission


class UniformPermission(BasePermission):
    permission_class = 'auth.uniform'


@extend_schema(tags=['uniforms'])
class UniformViewSet(ModelViewSet):
    queryset = Uniform.objects.all()

    permission_classes = [UniformPermission]
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
