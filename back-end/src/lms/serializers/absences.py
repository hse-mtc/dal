from rest_framework import serializers

from lms.models.common import Milgroup
from lms.models.students import Student
from lms.models.absences import (
    Absence,
    AbsenceTime,
)

from lms.serializers.students import StudentShortSerializer

from lms.validators import PresentInDatabaseValidator


class AbsenceSerializer(serializers.ModelSerializer):
    student = StudentShortSerializer()

    class Meta:
        model = Absence
        fields = "__all__"


class AbsenceMutateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Absence
        fields = "__all__"


class AbsenceJournalQuerySerializer(serializers.Serializer):
    milgroup = serializers.IntegerField(
        required=True, validators=[PresentInDatabaseValidator(Milgroup, "id")])
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)

    def validate(self, attrs):
        if attrs["date_from"] > attrs["date_to"]:
            raise serializers.ValidationError(
                "date_from should be greater or equal to date_to")
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class AbsenceShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Absence
        fields = ["id", "date", "excuse", "status", "reason", "comment"]


class AbsenceJournalSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField(read_only=True)
    absences = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ["id", "fullname", "absences"]

    def get_fullname(self, obj: Student) -> str:
        return obj.name.fullname

    def get_absences(self, obj):
        absences = obj.absence_set.filter(date__in=self.context["date_range"])
        return AbsenceShortSerializer(absences, many=True).data


class AbsenceTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AbsenceTime
        fields = "__all__"
