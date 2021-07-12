from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    IntegerField,
    CharField,
    ListField,
)

from lms.models.common import (
    Milfaculty,
    Milspecialty,
    Milgroup,
)


class MilfacultySerializer(ModelSerializer):

    class Meta:
        model = Milfaculty
        fields = "__all__"


class MilspecialtySerializer(ModelSerializer):

    class Meta:
        model = Milspecialty
        fields = "__all__"


class MilgroupSerializer(ModelSerializer):
    milfaculty = MilfacultySerializer(read_only=True)
    weekday = IntegerField(read_only=True)

    class Meta:
        model = Milgroup
        fields = "__all__"


class MilgroupMutateSerializer(ModelSerializer):

    class Meta:
        model = Milgroup
        fields = "__all__"


class MilgroupLeadersPhonesSerializer(Serializer):
    phones = ListField(child=CharField())

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
