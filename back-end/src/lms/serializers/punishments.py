from rest_framework.serializers import ModelSerializer

from common.serializers.populate import BaseMutateSerializer

from lms.models.punishments import Punishment

from lms.serializers.students import StudentShortSerializer
from lms.serializers.teachers import TeacherShortSerializer


class PunishmentSerializer(ModelSerializer):
    student = StudentShortSerializer()
    teacher = TeacherShortSerializer()

    class Meta:
        model = Punishment
        fields = "__all__"


class PunishmentMutateSerializer(BaseMutateSerializer):

    class Meta:
        model = Punishment
        fields = "__all__"
