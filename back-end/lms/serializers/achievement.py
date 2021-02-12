from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.serializers import ModelSerializer

from lms.models.student import Student
from lms.models.achievement import Achievement, AchievementType

from lms.validators import PresentInDatabaseValidator
from lms.serializers.student import StudentShortSerializer


class AchievementTypeSerializer(ModelSerializer):

    class Meta:
        model = AchievementType
        fields = '__all__'


class AchievementSerializer(WritableNestedModelSerializer):
    student = StudentShortSerializer(
        required=False, validators=[PresentInDatabaseValidator(Student)])

    class Meta:
        model = Achievement
        fields = '__all__'
