from rest_framework.serializers import (ModelSerializer, IntegerField,
                                        CharField)

from lms.models.common import Milgroup


class MilgroupSerializer(ModelSerializer):
    milgroup = IntegerField()
    milfaculty = CharField(required=False)
    weekday = IntegerField(required=False)

    class Meta:
        model = Milgroup
        fields = '__all__'
