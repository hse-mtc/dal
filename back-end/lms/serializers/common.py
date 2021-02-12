from rest_framework.serializers import (ModelSerializer, IntegerField,
                                        CharField)

from lms.models.common import Milgroup, Milfaculty


class MilfacultySerializer(ModelSerializer):

    class Meta:
        model = Milfaculty
        fields = '__all__'


class MilgroupSerializer(ModelSerializer):
    milgroup = IntegerField()
    milfaculty = CharField(required=False)
    weekday = IntegerField(required=False)

    class Meta:
        model = Milgroup
        fields = '__all__'
