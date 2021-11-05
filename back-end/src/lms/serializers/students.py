from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer

from common.serializers.milspecialties import MilspecialtySerializer
from common.serializers.universities import UniversityInfoSerializer
from common.serializers.personal import (
    BirthInfoSerializer,
    ContactInfoSerializer,
    PhotoSerializer,
    PhotoMutateMixin,
    RelativeMutateSerializer,
    PassportSerializer,
)

from lms.models.common import Milgroup
from lms.models.students import (
    Student,
    Skill,
    Note,
)

from lms.serializers.common import MilgroupSerializer


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True)
    milgroup = MilgroupSerializer(read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)

    skills = SkillSerializer(
        many=True,
        read_only=True,
    )

    photo = PhotoSerializer(read_only=True)
    birth_info = BirthInfoSerializer(read_only=True)
    university_info = UniversityInfoSerializer(read_only=True)

    class Meta:
        model = Student
        fields = "__all__"


class StudentMutateSerializer(
        WritableNestedModelSerializer,
        PhotoMutateMixin,
):
    milgroup = serializers.PrimaryKeyRelatedField(
        queryset=Milgroup.objects.all(),
        required=False,
    )

    passport = PassportSerializer(required=False)
    family = RelativeMutateSerializer(required=False, many=True)
    university_info = UniversityInfoSerializer(required=False)

    class Meta:
        model = Student
        fields = "__all__"

    def create(self, validated_data):
        corporate_email = validated_data["contact_info"]["corporate_email"]
        student_with_same_corporate_email = Student.objects.filter(
            contact_info__corporate_email=corporate_email)

        if student_with_same_corporate_email.exists():
            raise serializers.ValidationError(
                "Cannot create Student: this corporate email already exists")

        self.create_photo(validated_data)
        return super().create(validated_data)

    def update(self, instance: Student, validated_data):
        self.update_photo(instance, validated_data)
        return super().update(instance, validated_data)


class StudentShortSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True)
    milgroup = MilgroupSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ["id", "fullname", "milgroup"]


class StudentBasicInfoSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True)
    milgroup = MilgroupSerializer(read_only=True)
    photo = PhotoSerializer(read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)
    birth_info = BirthInfoSerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            "id", "fullname", "milgroup", "photo", "post", "contact_info",
            "status", "birth_info"
        ]


class StudentExtraInfoSerializer(serializers.ModelSerializer):
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


class StudentSkillsSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = Student
        fields = ["skills"]


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Note
        fields = "__all__"
