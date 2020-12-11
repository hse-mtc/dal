from drf_writable_nested.serializers import WritableNestedModelSerializer

from lms.models.student import Student
from lms.models.achievement import Achievement

from lms.validators import PresentInDatabaseValidator
from lms.serializers.student import StudentShortSerializer


class AchievementSerializer(WritableNestedModelSerializer):
    student = StudentShortSerializer(
        required=False, validators=[PresentInDatabaseValidator(Student)])

    class Meta:
        model = Achievement
        fields = '__all__'
