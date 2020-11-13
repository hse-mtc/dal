from rest_framework.serializers import (ModelSerializer, IntegerField,
                                        CharField)
from drf_writable_nested.serializers import WritableNestedModelSerializer

from lms.models import (
    TeacherPost,
    Milgroup,
    Program,
    Rank,
    Student,
    Punishment
)

from lms.validators import PresentInDatabaseValidator
from lms.serializers.student import StudentShortSerializer
from lms.serializers.teacher import TeacherShortSerializer


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
