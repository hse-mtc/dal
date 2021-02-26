from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.viewsets import ModelViewSet

from lms.models.students import Student
from lms.models.teachers import Teacher
from lms.models.punishments import Punishment, PunishmentType

from lms.validators import PresentInDatabaseValidator
from lms.serializers.student import StudentShortSerializer
from lms.serializers.teacher import TeacherShortSerializer


class PunishmentTypeSerializer(ModelViewSet):

    class Meta:
        model = PunishmentType
        fields = '__all__'


class PunishmentSerializer(WritableNestedModelSerializer):
    student = StudentShortSerializer(
        required=False, validators=[PresentInDatabaseValidator(Student)])
    teacher = TeacherShortSerializer(
        required=False, validators=[PresentInDatabaseValidator(Teacher)])

    class Meta:
        model = Punishment
        fields = '__all__'
