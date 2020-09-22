from rest_framework.serializers import ModelSerializer, IntegerField

from lms.models import (
    Milgroup,
    Program,
)


class MilgroupSerializer(ModelSerializer):
    milgroup = IntegerField()

    class Meta:
        model = Milgroup
        fields = '__all__'


class ProgramSerializer(ModelSerializer):

    class Meta:
        model = Program
        fields = '__all__'
        extra_kwargs = {'code': {'validators': []}}
