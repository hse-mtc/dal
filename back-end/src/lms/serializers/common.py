from rest_framework import serializers

from common.serializers.milspecialties import MilspecialtySerializer

from lms.models.common import (
    Milfaculty,
    Milgroup,
)


class MilfacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Milfaculty
        fields = "__all__"


class MilgroupSerializer(serializers.ModelSerializer):
    milfaculty = MilfacultySerializer(read_only=True)
    weekday = serializers.IntegerField(read_only=True)
    milspecialty = MilspecialtySerializer(read_only=True)

    class Meta:
        model = Milgroup
        fields = "__all__"


class MilgroupMutateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milgroup
        fields = "__all__"


class MilgroupLeadersPhonesSerializer(serializers.Serializer):
    phones = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
