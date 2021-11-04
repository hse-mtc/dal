import base64

from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer

from common.serializers.milspecialties import MilspecialtySerializer
from common.serializers.universities import UniversityInfoSerializer
from common.serializers.personal import (
    BirthInfoSerializer,
    ContactInfoSerializer,
    NameSerializer,
    PhotoMutateMixin,
    RelativeSerializer,
)

from ams.models.applicants import (
    RecruitmentOffice,
    ApplicationProcess,
    Applicant,
)


class RecruitmentOfficeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruitmentOffice
        exclude = ["id"]


class ApplicationProcessSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationProcess
        exclude = ["id"]


class ApplicantSerializer(serializers.ModelSerializer):
    name = NameSerializer(read_only=True)
    birth_info = BirthInfoSerializer(read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)
    university_info = UniversityInfoSerializer(read_only=True)

    photo = serializers.SerializerMethodField(read_only=True)

    family = RelativeSerializer(read_only=True, many=True)

    recruitment_office = RecruitmentOfficeSerializer(read_only=True)
    milspecialty = MilspecialtySerializer(read_only=True)

    def get_photo(self, obj: Applicant) -> str:
        return base64.b64encode(obj.photo.image.read()).decode()

    class Meta:
        model = Applicant
        exclude = ["id"]


class ApplicantMutateSerializer(
    WritableNestedModelSerializer,
    PhotoMutateMixin,
):

    class Meta:
        model = Applicant
        fields = "__all__"


class ApplicantWithApplicationProcessSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(
        read_only=True,
        source="name.fullname",
    )
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

    class Meta:
        model = Applicant
        fields = [
            "id",
            "full_name",
            "birth_date",
            "program_code",
            "faculty",
            "application_process",
        ]
