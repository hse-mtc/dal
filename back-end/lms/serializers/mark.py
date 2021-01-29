from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.serializers import ValidationError

from lms.models.lesson import Lesson
from lms.models.mark import Mark
from lms.models.student import Student
from lms.serializers.lesson import LessonSerializer
from lms.serializers.student import StudentShortSerializer

from lms.validators import PresentInDatabaseValidator


class MarkSerializer(WritableNestedModelSerializer):
    student = StudentShortSerializer(
        required=False, validators=[PresentInDatabaseValidator(Student)])
    lesson = LessonSerializer(
        required=False, validators=[PresentInDatabaseValidator(Lesson)])

    def validate(self, attrs):
        student_id = attrs['student']['id']
        student_milgroup = Student.objects.get(id=student_id).milgroup.milgroup
        lesson_id = attrs['lesson']['id']
        lesson_milgroup = Lesson.objects.get(id=lesson_id).milgroup.milgroup
        if student_milgroup != lesson_milgroup:
            raise ValidationError(
                'student milgroup and lesson milgroup should be equal')
        return attrs

    class Meta:
        model = Mark
        fields = '__all__'
