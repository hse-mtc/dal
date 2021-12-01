from rest_framework import serializers

from lms.models.common import Milgroup
from lms.models.lessons import (
    Room,
    Lesson,
)

from lms.serializers.subjects import LessonSubjectSerializer
from lms.serializers.common import MilgroupSerializer

from lms.validators import PresentInDatabaseValidator


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"


class LessonShortSerializer(serializers.ModelSerializer):
    subject = LessonSubjectSerializer(read_only=True)

    class Meta:
        model = Lesson
        exclude = ["milgroup"]


class LessonSerializer(serializers.ModelSerializer):
    subject = LessonSubjectSerializer(read_only=True)
    milgroup = MilgroupSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"


class LessonMutateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class LessonJournalQuerySerializer(serializers.Serializer):
    milgroup = serializers.IntegerField(
        required=True,
        validators=[PresentInDatabaseValidator(Milgroup, "id")],
    )
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)

    def validate(self, attrs):
        if attrs["date_from"] > attrs["date_to"]:
            raise ValueError(
                "date_to should be greater than or equal to date_from")
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
