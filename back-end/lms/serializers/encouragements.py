from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.serializers import ModelSerializer

from lms.models.encouragements import Encouragement

from lms.serializers.students import StudentShortSerializer
from lms.serializers.teachers import TeacherShortSerializer


class EncouragementSerializer(WritableNestedModelSerializer):
    student = StudentShortSerializer()
    teacher = TeacherShortSerializer()

    class Meta:
        model = Encouragement
        fields = '__all__'


class EncouragementMutateSerializer(ModelSerializer):

    class Meta:
        model = Encouragement
        fields = '__all__'
