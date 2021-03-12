from drf_writable_nested.serializers import WritableNestedModelSerializer
from common.serializers.populate import BaseMutateSerializer

from lms.models.punishments import Punishment

from lms.serializers.students import StudentShortSerializer
from lms.serializers.teachers import TeacherShortSerializer


class PunishmentSerializer(WritableNestedModelSerializer):
    student = StudentShortSerializer()
    teacher = TeacherShortSerializer()

    class Meta:
        model = Punishment
        fields = '__all__'


class PunishmentMutateSerializer(BaseMutateSerializer):

    class Meta:
        model = Punishment
        fields = '__all__'
