from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.serializers import ModelSerializer
from common.serializers.populate import BaseMutateSerializer

from lms.models.achievements import Achievement, AchievementType
from lms.serializers.students import StudentShortSerializer


class AchievementTypeSerializer(ModelSerializer):

    class Meta:
        model = AchievementType
        fields = '__all__'


class AchievementSerializer(WritableNestedModelSerializer):
    student = StudentShortSerializer()

    class Meta:
        model = Achievement
        fields = '__all__'


class AchievementMutateSerializer(BaseMutateSerializer):

    class Meta:
        model = Achievement
        fields = '__all__'
