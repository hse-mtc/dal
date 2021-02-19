from rest_framework.serializers import (ModelSerializer, Serializer,
                                        IntegerField, DateField)

from drf_writable_nested.serializers import WritableNestedModelSerializer

from common.models.subjects import Subject

from lms.validators import PresentInDatabaseValidator
from lms.serializers.subject import LessonSubjectSerializer
from lms.serializers.student import StudentShortSerializer
from lms.serializers.common import MilgroupSerializer
from lms.models.common import Milgroup
from lms.models.student import Student
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
    id = IntegerField(required=False)

    subject = LessonSubjectSerializer(
        required=False, validators=[PresentInDatabaseValidator(Subject)])
    milgroup = MilgroupSerializer(
        required=False, validators=[PresentInDatabaseValidator(Milgroup)])
    student = StudentShortSerializer(
        required=False, validators=[PresentInDatabaseValidator(Student)])

    # specify that this field is not required
    ordinal = IntegerField(required=False)

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonShortSerializer(LessonSerializer):
    milgroup = None

    class Meta:
        model = Lesson
        exclude = ['milgroup']


class LessonJournalGetQuerySerializer(Serializer):
    milgroup = IntegerField(
        required=True,
        validators=[PresentInDatabaseValidator(Milgroup, 'milgroup')])
    date_from = DateField(required=False)
    date_to = DateField(required=False)

    def validate(self, attrs):
        if attrs['date_from'] > attrs['date_to']:
            raise ValueError('date_from should be greater or equal to date_to')
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
