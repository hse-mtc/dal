from rest_framework.viewsets import ModelViewSet
from drf_spectacular.views import extend_schema

from lms.models.uniforms import Uniform
from lms.serializers.uniforms import UniformSerializer, UniformMutateSerializer

from common.constants import MUTATE_ACTIONS
from auth.permissions import BasicPermission


class UniformPermission(BasicPermission):
    permission_class = 'auth.uniform'


@extend_schema(tags=['uniforms'])
class UniformViewSet(ModelViewSet):
    queryset = Uniform.objects.all()

    permission_classes = [UniformPermission]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return UniformMutateSerializer
        return UniformSerializer
