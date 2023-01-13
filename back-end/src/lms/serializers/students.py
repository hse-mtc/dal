from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer

from auth.models import Group
from common.serializers.milspecialties import MilspecialtySerializer
from common.serializers.universities import (
    UniversityInfoSerializer,
    UniversityInfoMutateSerializer,
)
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
    contact_info = ContactInfoSerializer(required=False)

    birth_info = BirthInfoSerializer(required=False)
    passport = PassportSerializer(required=False)
    university_info = UniversityInfoMutateSerializer(required=False)
    family = RelativeMutateSerializer(required=False, many=True)

    class Meta:
        model = Student
        fields = "__all__"

    def create(self, validated_data):
        self.create_photo(validated_data)
        return super().create(validated_data)

    def update(self, instance: Student, validated_data):
        self.update_photo(instance, validated_data)
        return super().update(instance, validated_data)

    def validate(self, attrs):
        return super().validate(attrs)


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
            "id",
            "fullname",
            "milgroup",
            "photo",
            "post",
            "contact_info",
            "status",
            "birth_info",
        ]


class StudentExtraInfoSerializer(serializers.ModelSerializer):
    contact_info = ContactInfoSerializer(read_only=True)
    passport = PassportSerializer(read_only=True)
    university_info = UniversityInfoSerializer(read_only=True)
    milspecialty = MilspecialtySerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "contact_info",
            "milspecialty",
            "university_info",
            "citizenship",
            "permanent_address",
            "passport",
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


class ApproveStudentSerializer(serializers.ModelSerializer):
    milgroup = MilgroupSerializer(
        read_only=True,
    )
    email = serializers.CharField(
        read_only=True,
        source="user.email",
    )
    phone = serializers.CharField(
        read_only=True,
        source="contact_info.personal_phone_number",
    )

    class Meta:
        model = Student
        fields = [
            "id",
            "fullname",
            "milgroup",
            "post",
            "email",
            "phone",
        ]


class ApproveStudentMutateSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance: Student, validated_data):
        user = instance.user
        user.is_active = True
        user.groups.set(Group.objects.filter(name="Студент"))
        user.save()
        return instance
