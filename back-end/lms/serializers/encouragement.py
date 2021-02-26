from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.viewsets import ModelViewSet

from lms.models.students import Student
from lms.models.teachers import Teacher
from lms.models.encouragements import Encouragement, EncouragementType

from lms.validators import PresentInDatabaseValidator
from lms.serializers.student import StudentShortSerializer
from lms.serializers.teacher import TeacherShortSerializer


class EncouragementTypeSerializer(ModelViewSet):

    class Meta:
        model = EncouragementType
        fields = '__all__'


class EncouragementSerializer(WritableNestedModelSerializer):
    student = StudentShortSerializer(
        required=False, validators=[PresentInDatabaseValidator(Student)])
    teacher = TeacherShortSerializer(
        required=False, validators=[PresentInDatabaseValidator(Teacher)])

    class Meta:
        model = Encouragement
        fields = '__all__'
