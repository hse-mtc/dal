from rest_framework.serializers import (ModelSerializer, IntegerField, 
                                        CharField)

from lms.models import (
    Milgroup,
    Program,
)


class MilgroupSerializer(ModelSerializer):
    milgroup = IntegerField()
    milfaculty = CharField(required=False)

    class Meta:
        model = Milgroup
        fields = '__all__'


class ProgramSerializer(ModelSerializer):

    class Meta:
        model = Program
        fields = '__all__'
        extra_kwargs = {'code': {'validators': []}}
