from rest_framework import serializers

from common.models.subjects import Subject

from auth.serializers import UserSerializer


class LessonSubjectSerializer(serializers.ModelSerializer):
    user = UserSerializer(write_only=True,
                          default=serializers.CurrentUserDefault())
    title = serializers.CharField(required=False)

    class Meta:
        model = Subject
        fields = '__all__'
