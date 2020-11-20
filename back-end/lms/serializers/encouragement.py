from drf_writable_nested.serializers import WritableNestedModelSerializer

from lms.models.student import Student
from lms.models.teacher import Teacher
from lms.models.encouragement import Encouragement

from lms.validators import PresentInDatabaseValidator
from lms.serializers.student import StudentShortSerializer
from lms.serializers.teacher import TeacherShortSerializer


class EncouragementSerializer(WritableNestedModelSerializer):
    student = StudentShortSerializer(
        required=False, validators=[PresentInDatabaseValidator(Student)])
    teacher = TeacherShortSerializer(
        required=False, validators=[PresentInDatabaseValidator(Teacher)])

    class Meta:
        model = Encouragement
        fields = '__all__'
