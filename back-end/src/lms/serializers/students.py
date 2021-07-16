from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ImageField,
    PrimaryKeyRelatedField,
    BooleanField,
)

from drf_writable_nested.serializers import WritableNestedModelSerializer

from common.models.persons import Photo
from common.serializers.persons import (
    BirthInfoSerializer,
    RelativeMutateSerializer,
    PersonnelMutateSerializer,
    ContactInfoSerializer,
)

from lms.models.common import Milgroup
from lms.models.students import (
    Student,
    Skill,
    Note,
)
from lms.serializers.common import (
    MilgroupSerializer,
    MilspecialtySerializer,
)
from lms.serializers.applicants import (
    PassportSerializer,
    RecruitmentOfficeSerializer,
    ApplicationProcessSerializer,
)
from lms.serializers.universities import (
    UniversityInfoSerializer,
    UniversityInfoCreateSerializer,
)


class PhotoSerializer(ModelSerializer):
    image = ImageField(
        use_url=True,
        allow_null=True,
        required=False,
        read_only=True,
    )

    class Meta:
        model = Photo
        exclude = ["id"]


class SkillSerializer(ModelSerializer):

    class Meta:
        model = Skill
        fields = "__all__"


class StudentSerializer(ModelSerializer):
    fullname = SerializerMethodField(read_only=True)
    photo = PhotoSerializer(read_only=True)

    milgroup = MilgroupSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    birth_info = BirthInfoSerializer(read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)
    university_info = UniversityInfoSerializer(read_only=True)

    application_process = ApplicationProcessSerializer(read_only=False)

    class Meta:
        model = Student
        fields = "__all__"

    def get_fullname(self, obj):
        return f"{obj.surname} {obj.name} {obj.patronymic}"


class StudentMutateSerializer(
        WritableNestedModelSerializer,
        PersonnelMutateSerializer,
):
    milgroup = PrimaryKeyRelatedField(
        queryset=Milgroup.objects.all(),
        required=False,
    )

    passport = PassportSerializer(required=False)
    family = RelativeMutateSerializer(required=False, many=True)
    recruitment_office = RecruitmentOfficeSerializer(required=False)
    university_info = UniversityInfoCreateSerializer(required=False)

    # Send documents to `watchdoc`.
    generate_documents = BooleanField(default=False, write_only=True)

    class Meta(PersonnelMutateSerializer.Meta):
        model = Student
        exclude = ["application_process"]

    def create(self, validated_data):
        corporate_email = validated_data["contact_info"]["corporate_email"]
        find_student_filter = Student.objects.filter(
            contact_info__corporate_email=corporate_email)

        if find_student_filter.exists():
            instance = find_student_filter.last()
            return self.update(instance, validated_data)

        self.create_photo(validated_data)
        return super().create(validated_data)

    def update(self, instance: Student, validated_data):
        self.update_photo(instance, validated_data)
        return super().update(instance, validated_data)


class StudentShortSerializer(ModelSerializer):
    fullname = SerializerMethodField(read_only=True)
    milgroup = MilgroupSerializer(read_only=True)

    def get_fullname(self, obj):
        return f"{obj.surname} {obj.name} {obj.patronymic}"

    class Meta:
        model = Student
        fields = ["id", "fullname", "milgroup"]


class StudentBasicInfoSerializer(ModelSerializer):
    fullname = SerializerMethodField(read_only=True)
    milgroup = MilgroupSerializer(read_only=True)
    photo = PhotoSerializer(read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)
    birth_info = BirthInfoSerializer(read_only=True)

    def get_fullname(self, obj):
        return f"{obj.surname} {obj.name} {obj.patronymic}"

    class Meta:
        model = Student
        fields = [
            "id", "fullname", "milgroup", "photo", "post", "contact_info",
            "status", "birth_info"
        ]


class StudentExtraInfoSerializer(ModelSerializer):
    contact_info = ContactInfoSerializer(read_only=True)
    passport = PassportSerializer(read_only=True)
    university_info = UniversityInfoSerializer(read_only=True)
    milspecialty = MilspecialtySerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            "id", "contact_info", "milspecialty", "university_info",
            "citizenship", "permanent_address", "passport"
        ]


class StudentSkillsSerializer(ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = Student
        fields = ["skills"]


class NoteSerializer(ModelSerializer):

    class Meta:
        model = Note
        fields = "__all__"
