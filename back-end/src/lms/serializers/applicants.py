import base64

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateField,
    CharField,
)

from common.serializers.persons import (
    BirthInfoSerializer,
    ContactInfoSerializer,
    RelativeSerializer,
)

from lms.models.students import Student
from lms.models.applicants import (
    Passport,
    RecruitmentOffice,
    ApplicationProcess,
)

from lms.serializers.common import MilspecialtySerializer
from lms.serializers.universities import UniversityInfoSerializer


class PassportSerializer(ModelSerializer):

    class Meta:
        model = Passport
        exclude = ["id"]


class RecruitmentOfficeSerializer(ModelSerializer):

    class Meta:
        model = RecruitmentOffice
        exclude = ["id"]


class ApplicationProcessSerializer(ModelSerializer):

    class Meta:
        model = ApplicationProcess
        exclude = ["id"]


class ApplicantSerializer(ModelSerializer):
    birth_info = BirthInfoSerializer(read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)
    university_info = UniversityInfoSerializer(read_only=True)

    photo = SerializerMethodField(read_only=True)

    family = RelativeSerializer(read_only=True, many=True)

    recruitment_office = RecruitmentOfficeSerializer(read_only=True)
    milspecialty = MilspecialtySerializer(read_only=True)

    def get_photo(self, obj: Student) -> str:
        return base64.b64encode(obj.photo.image.read()).decode()

    class Meta:
        model = Student
        exclude = ["id"]


class ApplicantWithApplicationSerializer(ModelSerializer):
    full_name = CharField(read_only=True)
    birth_date = DateField(
        source="birth_info.date",
        read_only=True,
    )
    program_code = CharField(
        source="university_info.program.code",
        read_only=True,
    )
    faculty = CharField(
        source="university_info.program.faculty",
        read_only=True,
    )
    application_process = ApplicationProcessSerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            "full_name",
            "birth_date",
            "program_code",
            "faculty",
            "application_process",
        ]
