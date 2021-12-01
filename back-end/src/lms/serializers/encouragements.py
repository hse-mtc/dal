from rest_framework import serializers

from lms.models.encouragements import Encouragement

from lms.serializers.students import StudentShortSerializer
from lms.serializers.teachers import TeacherShortSerializer


class EncouragementSerializer(serializers.ModelSerializer):
    student = StudentShortSerializer(read_only=True)
    teacher = TeacherShortSerializer(read_only=True)

    class Meta:
        model = Encouragement
        fields = "__all__"


class EncouragementMutateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Encouragement
        fields = "__all__"
