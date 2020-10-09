from rest_framework.serializers import SerializerMethodField
from drf_writable_nested.serializers import WritableNestedModelSerializer

from lms.models import (
    Milgroup,
    Teacher,
)

from lms.validators import PresentInDatabaseValidator
from lms.serializers.serializers import MilgroupSerializer


class TeacherSerializer(WritableNestedModelSerializer):
    milgroup = MilgroupSerializer(
        required=False,
        many=False,
        validators=[PresentInDatabaseValidator(Milgroup)])

    fullname = SerializerMethodField(required=False)

    class Meta:
        model = Teacher
        fields = '__all__'

    def get_fullname(self, obj):
        # pylint: disable=(no-self-use)
        return f'{obj.surname} {obj.name} {obj.patronymic}'
