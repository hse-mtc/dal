from rest_framework.serializers import IntegerField, SerializerMethodField
from drf_writable_nested.serializers import WritableNestedModelSerializer

from lms.models import (
    Milgroup,
    Teacher,
)

from lms.validators import PresentInDatabaseValidator
from lms.serializers.serializers import MilgroupSerializer


class TeacherSerializer(WritableNestedModelSerializer):
    fullname = SerializerMethodField(required=False)
    milgroup = MilgroupSerializer(
        required=False,
        many=False,
        validators=[PresentInDatabaseValidator(Milgroup)])

    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

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
