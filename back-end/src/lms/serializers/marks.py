from rest_framework import serializers

from common.models.subjects import Subject

from lms.models.common import Milgroup
from lms.models.marks import (
    Mark,
    HistoricalMark,
)
from lms.models.students import Student
from lms.serializers.history import HistoricalRecordField

from lms.serializers.lessons import LessonSerializer
from lms.serializers.students import StudentShortSerializer

from lms.validators import PresentInDatabaseValidator


class MarkSerializer(serializers.ModelSerializer):
    student = StudentShortSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    history = HistoricalRecordField(read_only=True)
    changed_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Mark
        fields = "__all__"


class MarkMutateSerializer(serializers.ModelSerializer):
    values = serializers.ListField(
        child=serializers.IntegerField(min_value=2, max_value=5)
    )

    def validate(self, attrs):
        if "student" in attrs and "lesson" in attrs:
            if attrs["student"].milgroup != attrs["lesson"].milgroup:
                raise serializers.ValidationError(
                    "student milgroup and lesson milgroup should be equal"
                )
        return attrs

    class Meta:
        model = Mark
        fields = ["student", "lesson", "values", "changed_by"]


class MarkJournalQuerySerializer(serializers.Serializer):
    milgroup = serializers.IntegerField(
        required=True,
        validators=[PresentInDatabaseValidator(Milgroup, "id")],
    )
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    subject = serializers.IntegerField(
        required=True,
        validators=[PresentInDatabaseValidator(Subject, "id")],
    )

    def validate(self, attrs):
        if attrs["date_from"] > attrs["date_to"]:
            raise serializers.ValidationError(
                "date_from should be greater or equal to date_to"
            )
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class MarkShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ["id", "values", "lesson"]


class MarkHistorySerializer(serializers.ModelSerializer):
    student = StudentShortSerializer(read_only=True)
    teacher = serializers.SerializerMethodField(read_only=True)

    after = serializers.SerializerMethodField(read_only=True)
    before = serializers.SerializerMethodField(read_only=True)

    def get_after(self, obj):
        return obj.values

    def get_before(self, obj):
        prev_record = obj.prev_record
        if prev_record:
            return prev_record.values
        return None

    def get_teacher(self, obj):
        return obj.changed_by

    class Meta:
        model = HistoricalMark
        fields = [
            "after",
            "before",
            "student",
            "teacher",
        ]


class MarkJournalSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True)
    marks = serializers.SerializerMethodField(read_only=True)

    def get_marks(self, obj):
        marks = obj.mark_set.filter(
            lesson__date__in=self.context["date_range"],
            lesson__subject__id=self.context["subject"],
        )
        return MarkShortSerializer(marks, many=True).data

    class Meta:
        model = Student
        fields = ["id", "fullname", "marks"]
