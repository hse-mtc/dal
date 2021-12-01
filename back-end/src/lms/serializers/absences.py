from rest_framework import serializers

from lms.models.common import Milgroup
from lms.models.students import Student
from lms.models.absences import (
    Absence,
    AbsenceTime,
    AbsenceAttachment,
)

from lms.serializers.students import StudentShortSerializer

from lms.validators import PresentInDatabaseValidator


class AbsenceAttachmentSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        use_url=True,
        allow_null=True,
        required=False,
        read_only=True,
    )

    class Meta:
        model = AbsenceAttachment
        fields = "__all__"


class AbsenceSerializer(serializers.ModelSerializer):
    student = StudentShortSerializer()
    attachment = AbsenceAttachmentSerializer(read_only=True)

    class Meta: 
        model = Absence
        fields = "__all__"


class AbsenceMutateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)

    def create(self, validated_data):
        if image := validated_data.pop("image", None):
            absence_attachment = AbsenceAttachment.objects.create(image=image)
            validated_data["attachment"] = absence_attachment
        return super().create(validated_data)

    def update(self, instance: Absence, validated_data):
        if image := validated_data.pop("image", None):
            if instance.attachment:
                instance.attachment.image = image
                instance.attachment.save()
            else:
                instance.attachment = AbsenceAttachment.objects.create(image=image)
        return super().update(instance, validated_data)

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
    fullname = serializers.CharField(read_only=True)
    absences = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ["id", "fullname", "absences"]

    def get_absences(self, obj):
        absences = obj.absence_set.filter(date__in=self.context["date_range"])
        return AbsenceShortSerializer(absences, many=True).data


class AbsenceTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AbsenceTime
        fields = "__all__"
