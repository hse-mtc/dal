from rest_framework.serializers import (ModelSerializer, Serializer,
                                        IntegerField, DateField)

from drf_writable_nested.serializers import WritableNestedModelSerializer

from lms.validators import PresentInDatabaseValidator
from lms.serializers.subjects import LessonSubjectSerializer
from lms.serializers.students import StudentShortSerializer
from lms.serializers.common import MilgroupSerializer
from lms.models.common import Milgroup
from lms.models.lessons import Room, Lesson


class RoomSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'


class LessonSerializer(WritableNestedModelSerializer):
    subject = LessonSubjectSerializer()
    milgroup = MilgroupSerializer()
    student = StudentShortSerializer()

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonMutateSerializer(ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonShortSerializer(LessonSerializer):
    milgroup = None

    class Meta:
        model = Lesson
        exclude = ['milgroup']


class LessonJournalQuerySerializer(Serializer):
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
