from rest_framework import serializers

from lms.models.uniforms import Uniform

from lms.serializers.common import MilfacultySerializer


class UniformSerializer(serializers.ModelSerializer):
    milfaculty = MilfacultySerializer(read_only=True)

    class Meta:
        model = Uniform
        fields = "__all__"


class UniformMutateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uniform
        fields = "__all__"
