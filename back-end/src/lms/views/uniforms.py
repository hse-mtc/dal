from rest_framework.viewsets import ModelViewSet
from drf_spectacular.views import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from lms.models.uniforms import Uniform
from lms.serializers.uniforms import UniformSerializer, UniformMutateSerializer
from lms.filters.uniforms import UniformFilter

from common.constants import MUTATE_ACTIONS
from auth.permissions import BasicPermission


class UniformPermission(BasicPermission):
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
