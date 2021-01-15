from rest_framework.serializers import ModelSerializer

from drf_writable_nested.serializers import WritableNestedModelSerializer

from common.models.subjects import Subject

from lms.validators import PresentInDatabaseValidator
from lms.serializers.subject import LessonSubjectSerializer
from lms.serializers.common import MilgroupSerializer
from lms.models.common import Milgroup
from lms.models.lesson import Room, LessonType, Lesson


class RoomSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'


class LessonTypeSerializer(ModelSerializer):

    class Meta:
        model = LessonType
        fields = '__all__'


class LessonSerializer(WritableNestedModelSerializer):
    subject = LessonSubjectSerializer(
        required=False, validators=[PresentInDatabaseValidator(Subject)])
    milgroup = MilgroupSerializer(
        required=False, validators=[PresentInDatabaseValidator(Milgroup)])

    class Meta:
        model = Lesson
        fields = '__all__'
