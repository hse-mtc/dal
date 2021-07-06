from rest_framework.serializers import (ModelSerializer, IntegerField,
                                        CharField,)

from lms.models.common import (
    Milfaculty,
    Milspecialty,
    Milgroup,
)
from lms.validators import PresentInDatabaseValidator


class MilfacultySerializer(ModelSerializer):

    class Meta:
        model = Milfaculty
        fields = '__all__'


class MilspecialtySerializer(ModelSerializer):

    class Meta:
        model = Milspecialty
        fields = '__all__'


class MilgroupSerializer(ModelSerializer):
    milgroup = IntegerField()
    milfaculty = CharField(required=False)
    weekday = IntegerField(required=False)

    class Meta:
        model = Milgroup
        fields = '__all__'


class MilgroupMutateSerializer(ModelSerializer):
    milgroup = IntegerField()
    milfaculty = CharField(validators=[PresentInDatabaseValidator(Milfaculty, "milfaculty")])
    weekday = IntegerField()

    def create_valid_data(self, validated_data: dict) -> dict:
        milfaculty = validated_data.pop("milfaculty")
        query = Milfaculty.objects.filter(milfaculty=milfaculty)
        validated_data["milfaculty"] = query.first()
        return validated_data

    def create(self, validated_data):
        return super().create(self.create_valid_data(validated_data))

    def update(self, instance, validated_data):
        return super().update(instance, self.create_valid_data(validated_data))

    class Meta:
        model = Milgroup
        fields = '__all__'
