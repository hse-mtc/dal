import base64

from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer

from ams.utils.common import get_current_admission_year
from common.serializers.milspecialties import MilspecialtySerializer
from common.serializers.universities import (
    UniversityInfoSerializer,
    UniversityInfoMutateSerializer,
)
from common.serializers.personal import (
    BirthInfoSerializer,
    ContactInfoSerializer,
    PhotoMutateMixin,
    RelativeSerializer,
    PassportSerializer,
    PersonalDocumentsInfoSerializer,
    RelativeMutateSerializer,
)

from ams.models.applicants import (
    ApplicationProcess,
    Applicant,
)


class ApplicationProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationProcess
        exclude = ["id"]

    def create(self, validated_data):
        cur_adm_year = get_current_admission_year()
        validated_data["mtc_admission_year"] = validated_data.get(
            "mtc_admission_year", cur_adm_year
        )
        return super().create(validated_data)


class ApplicantSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True)
    birth_info = BirthInfoSerializer(read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)
    university_info = UniversityInfoSerializer(read_only=True)
    passport = PassportSerializer(read_only=True)
    personal_documents_info = PersonalDocumentsInfoSerializer(read_only=True)
    photo = serializers.SerializerMethodField(read_only=True)
    marital_status = serializers.SerializerMethodField(read_only=True)

    family = RelativeSerializer(read_only=True, many=True)

    milspecialty = MilspecialtySerializer(read_only=True)

    def get_marital_status(self, obj):
        return obj.get_marital_status_display()

    def get_photo(self, obj: Applicant) -> str:
        return base64.b64encode(obj.photo.image.read()).decode()

    class Meta:
        model = Applicant
        exclude = ["id"]


class ApplicantMutateSerializer(
    WritableNestedModelSerializer,
    PhotoMutateMixin,
):
    birth_info = BirthInfoSerializer(required=False)
    passport = PassportSerializer(required=False)
    personal_documents_info = PersonalDocumentsInfoSerializer(required=False)
    university_info = UniversityInfoMutateSerializer(required=False)
    contact_info = ContactInfoSerializer(required=False)
    family = RelativeMutateSerializer(required=False, many=True)
    generate_documents = serializers.BooleanField(required=False)

    class Meta:
        model = Applicant
        exclude = ["application_process"]

    def create(self, validated_data):
        self.create_photo(validated_data)
        return super().create(validated_data)

    def update(self, instance: Applicant, validated_data):
        self.update_photo(instance, validated_data)
        return super().update(instance, validated_data)


class ApplicantWithApplicationProcessSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True)
    birth_date = serializers.DateField(
        read_only=True,
        source="birth_info.date",
    )
    program_code = serializers.CharField(
        read_only=True,
        source="university_info.program.code",
    )
    faculty = serializers.CharField(
        read_only=True,
        source="university_info.program.faculty.title",
    )
    application_process = ApplicationProcessSerializer(read_only=True)
    marital_status = serializers.SerializerMethodField(read_only=True)

    def get_marital_status(self, obj):
        return obj.get_marital_status_display()

    class Meta:
        model = Applicant
        fields = [
            "id",
            "fullname",
            "birth_date",
            "program_code",
            "faculty",
            "application_process",
            "marital_status",
        ]
