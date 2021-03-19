from rest_framework.serializers import (ModelSerializer, IntegerField,
                                        CharField)

from lms.models.common import (
    Milfaculty,
    Milspecialty,
    Milgroup,
)


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
