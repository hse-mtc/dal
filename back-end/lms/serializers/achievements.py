from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.serializers import ModelSerializer

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


class AchievementMutateSerializer(ModelSerializer):

    class Meta:
        model = Achievement
        fields = '__all__'
