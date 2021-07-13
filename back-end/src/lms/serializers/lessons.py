from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    IntegerField,
    DateField,
)

from common.serializers.populate import BaseMutateSerializer

from lms.validators import PresentInDatabaseValidator

from lms.serializers.subjects import LessonSubjectSerializer
from lms.serializers.common import MilgroupSerializer

from lms.models.common import Milgroup
from lms.models.lessons import Room, Lesson


class RoomSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"


class LessonShortSerializer(ModelSerializer):
    subject = LessonSubjectSerializer(read_only=True)

    class Meta:
        model = Lesson
        exclude = ["milgroup"]


class LessonSerializer(ModelSerializer):
    subject = LessonSubjectSerializer(read_only=True)
    milgroup = MilgroupSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"


class LessonMutateSerializer(BaseMutateSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class LessonJournalQuerySerializer(Serializer):
    milgroup = IntegerField(
        required=True, validators=[PresentInDatabaseValidator(Milgroup, "id")])
    date_from = DateField(required=False)
    date_to = DateField(required=False)

    def validate(self, attrs):
        if attrs["date_from"] > attrs["date_to"]:
            raise ValueError(
                "date_to should be greater than or equal to date_from")
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
