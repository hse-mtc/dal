from rest_framework.serializers import ModelSerializer

from common.serializers.populate import BaseMutateSerializer

from lms.models.uniforms import Uniform
from lms.serializers.common import MilfacultySerializer


class UniformSerializer(ModelSerializer):
    milfaculty = MilfacultySerializer(read_only=True)

    class Meta:
        model = Uniform
        fields = "__all__"


class UniformMutateSerializer(BaseMutateSerializer):

    class Meta:
        model = Uniform
        fields = "__all__"
