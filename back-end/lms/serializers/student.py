from rest_framework.serializers import IntegerField, SerializerMethodField
from drf_writable_nested.serializers import WritableNestedModelSerializer

from lms.models.common import Milgroup
from lms.models.student import Program, Student

from lms.validators import PresentInDatabaseValidator
from lms.serializers.common import MilgroupSerializer


class ProgramSerializer(ModelSerializer):

    class Meta:
        model = Program
        fields = '__all__'
        extra_kwargs = {'code': {'validators': []}}


class StudentSerializer(WritableNestedModelSerializer):
    milgroup = MilgroupSerializer(
        required=False, validators=[PresentInDatabaseValidator(Milgroup)])
    program = ProgramSerializer(
        required=False, validators=[PresentInDatabaseValidator(Program)])

    fullname = SerializerMethodField(required=False)

    class Meta:
        model = Student
        fields = '__all__'

    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'


class StudentShortSerializer(WritableNestedModelSerializer):
    id = IntegerField(required=False)
    fullname = SerializerMethodField(required=False)
    milgroup = MilgroupSerializer(
        many=False,
        required=False,
        validators=[PresentInDatabaseValidator(Milgroup)])

    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    class Meta:
        model = Student
        fields = ['id', 'fullname', 'milgroup']
