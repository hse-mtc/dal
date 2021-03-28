import base64

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from lms.models.students import Student

from common.serializers.persons import (
    BirthInfoSerializer,
    ContactInfoSerializer,
    RelativeSerializer,
)
from lms.serializers.common import MilspecialtySerializer
from lms.serializers.students import RecruitmentOfficeSerializer
from lms.serializers.universities import (
    UniversityInfoSerializer,
)


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
