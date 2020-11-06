from rest_framework.serializers import (ModelSerializer, IntegerField,
                                        CharField)

from lms.models import (
    TeacherPost,
    Milgroup,
    Program,
    Rank,
)


class MilgroupSerializer(ModelSerializer):
    milgroup = IntegerField()
    milfaculty = CharField(required=False)
    weekday = IntegerField(required=False)

    class Meta:
        model = Milgroup
        fields = '__all__'


class ProgramSerializer(ModelSerializer):

    class Meta:
        model = Program
        fields = '__all__'
        extra_kwargs = {'code': {'validators': []}}


class RankSerializer(ModelSerializer):

    class Meta:
        model = Rank
        fields = '__all__'


class TeacherPostSerializer(ModelSerializer):

    class Meta:
        model = TeacherPost
        fields = '__all__'
