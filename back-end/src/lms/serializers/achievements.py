from rest_framework import serializers

from lms.models.achievements import (
    Achievement,
    AchievementType,
)

from lms.serializers.students import StudentShortSerializer


class AchievementTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AchievementType
        fields = "__all__"


class AchievementSerializer(serializers.ModelSerializer):
    student = StudentShortSerializer(read_only=True)
    type = AchievementTypeSerializer(read_only=True)

    class Meta:
        model = Achievement
        fields = "__all__"


class AchievementMutateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = "__all__"
