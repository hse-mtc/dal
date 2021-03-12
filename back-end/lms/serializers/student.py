from rest_framework.serializers import (
    IntegerField,
    SerializerMethodField,
    ModelSerializer,
)
from drf_writable_nested.serializers import WritableNestedModelSerializer
from common.models.persons import Relative

from lms.models.common import Milgroup
from lms.models.student import (
    Program,
    Student,
    Passport,
    Family,
    RecruitmentOffice,
    UniversityInfo,
)

from lms.validators import PresentInDatabaseValidator
from lms.serializers.common import MilgroupSerializer


class ProgramSerializer(ModelSerializer):

    class Meta:
        model = Program
        fields = '__all__'
        extra_kwargs = {'code': {'validators': []}}


class PassportSerializer(ModelSerializer):

    class Meta:
        model = Passport
        exclude = ['id']


class RelativeSerializer(ModelSerializer):

    class Meta:
        model = Relative
        exclude = ['id']


class FamilySerializer(ModelSerializer):
    mother = RelativeSerializer()
    father = RelativeSerializer()
    brothers = RelativeSerializer(many=True)
    sisters = RelativeSerializer(many=True)

    class Meta:
        model = Family
        exclude = ['id']


class RecruitmentOfficeSerializer(ModelSerializer):

    class Meta:
        model = RecruitmentOffice
        exclude = ['id']


class UniversityInfoSerializer(ModelSerializer):

    class Meta:
        model = UniversityInfo
        exclude = ['id']


class StudentSerializer(WritableNestedModelSerializer):
    milgroup = MilgroupSerializer(
        required=False, validators=[PresentInDatabaseValidator(Milgroup)])

    program = ProgramSerializer(
        required=False, validators=[PresentInDatabaseValidator(Program)])

    recruitment_office = RecruitmentOfficeSerializer(
        required=False,
        validators=[PresentInDatabaseValidator(RecruitmentOffice)])

    university_info = UniversityInfoSerializer(
        required=False, validators=[PresentInDatabaseValidator(Family)])

    passport = PassportSerializer(required=False)

    family = FamilySerializer(required=False)

    fullname = SerializerMethodField(required=False)

    class Meta:
        model = Student
        fields = '__all__'

    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'


class StudentShortSerializer(WritableNestedModelSerializer):
    id = IntegerField(required=True)
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
