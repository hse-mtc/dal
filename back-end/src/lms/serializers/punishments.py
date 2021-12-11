from rest_framework import serializers

from lms.models.punishments import Punishment

from lms.serializers.students import StudentShortSerializer
from lms.serializers.teachers import TeacherShortSerializer


class PunishmentSerializer(serializers.ModelSerializer):
    student = StudentShortSerializer(read_only=True)
    teacher = TeacherShortSerializer(read_only=True)

    class Meta:
        model = Punishment
        fields = "__all__"


class PunishmentMutateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Punishment
        fields = "__all__"
