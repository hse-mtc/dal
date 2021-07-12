from rest_framework.serializers import ModelSerializer

from common.serializers.populate import BaseMutateSerializer

from lms.models.encouragements import Encouragement

from lms.serializers.students import StudentShortSerializer
from lms.serializers.teachers import TeacherShortSerializer


class EncouragementSerializer(ModelSerializer):
    student = StudentShortSerializer(read_only=True)
    teacher = TeacherShortSerializer(read_only=True)

    class Meta:
        model = Encouragement
        fields = "__all__"


class EncouragementMutateSerializer(BaseMutateSerializer):

    class Meta:
        model = Encouragement
        fields = "__all__"
