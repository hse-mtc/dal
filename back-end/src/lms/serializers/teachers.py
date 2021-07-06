from rest_framework.serializers import (IntegerField, SerializerMethodField,
                                        ModelSerializer)
from drf_writable_nested.serializers import WritableNestedModelSerializer
from common.serializers.populate import BaseMutateSerializer
from common.serializers.persons import BirthInfoSerializer

from lms.models.common import Milgroup
from lms.models.teachers import Rank, TeacherPost, Teacher

from lms.validators import PresentInDatabaseValidator
from lms.serializers.common import MilgroupSerializer


class RankSerializer(ModelSerializer):

    class Meta:
        model = Rank
        fields = '__all__'


class TeacherPostSerializer(ModelSerializer):

    class Meta:
        model = TeacherPost
        fields = '__all__'


class TeacherSerializer(WritableNestedModelSerializer):
    fullname = SerializerMethodField(required=False)
    milgroup = MilgroupSerializer()

    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherMutateSerializer(WritableNestedModelSerializer,
                              BaseMutateSerializer):
    birth_info = BirthInfoSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherShortSerializer(WritableNestedModelSerializer):
    id = IntegerField(required=False)
    fullname = SerializerMethodField(required=False)
    milgroup = MilgroupSerializer(
        required=False,
        many=False,
        validators=[PresentInDatabaseValidator(Milgroup)])

    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    class Meta:
        model = Teacher
        fields = ['id', 'fullname', 'milgroup']
