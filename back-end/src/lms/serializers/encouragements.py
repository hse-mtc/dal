from drf_writable_nested import WritableNestedModelSerializer
from common.serializers.populate import BaseMutateSerializer

from lms.models.encouragements import Encouragement

from lms.serializers.students import StudentShortSerializer
from lms.serializers.teachers import TeacherShortSerializer


class EncouragementSerializer(WritableNestedModelSerializer):
    student = StudentShortSerializer()
    teacher = TeacherShortSerializer()

    class Meta:
        model = Encouragement
        fields = '__all__'


class EncouragementMutateSerializer(BaseMutateSerializer):

    class Meta:
        model = Encouragement
        fields = '__all__'
