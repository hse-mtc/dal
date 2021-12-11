from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer

from common.serializers.personal import (
    BirthInfoSerializer,
    ContactInfoSerializer,
    PhotoMutateMixin,
)

from auth.models import Group

from lms.models.common import Milgroup
from lms.models.teachers import Teacher

from lms.serializers.students import PhotoSerializer
from lms.serializers.common import (
    MilgroupSerializer,
    MilfacultySerializer,
)

from lms.validators import PresentInDatabaseValidator


class TeacherSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True)
    milgroups = MilgroupSerializer(read_only=True, many=True)
    milfaculty = MilfacultySerializer(read_only=True)
    birth_info = BirthInfoSerializer(read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)
    photo = PhotoSerializer(read_only=True)

    class Meta:
        model = Teacher
        fields = "__all__"


class TeacherMutateSerializer(
    PhotoMutateMixin,
    WritableNestedModelSerializer,
):
    birth_info = BirthInfoSerializer(required=False)
    contact_info = ContactInfoSerializer()

    class Meta:
        model = Teacher
        fields = "__all__"

    def create(self, validated_data):
        self.create_photo(validated_data)
        return super().create(validated_data)

    def update(self, instance: Teacher, validated_data):
        self.update_photo(instance, validated_data)
        return super().update(instance, validated_data)


class TeacherShortSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True)
    milgroups = MilgroupSerializer(
        read_only=True,
        many=True,
        # TODO(TmLev): This is probably unnecessary.
        validators=[PresentInDatabaseValidator(Milgroup)],
    )

    class Meta:
        model = Teacher
        fields = ["id", "fullname", "milgroups"]


class ApproveTeacherSerializer(serializers.ModelSerializer):
    milfaculty = MilfacultySerializer(read_only=True)
    milgroups = MilgroupSerializer(
        read_only=True,
        many=True,
    )
    email = serializers.CharField(
        read_only=True,
        source="user.email",
    )

    class Meta:
        model = Teacher
        fields = [
            "id",
            "fullname",
            "milfaculty",
            "milgroups",
            "post",
            "rank",
            "email",
        ]


class ApproveTeacherMutateSerializer(serializers.Serializer):
    permission_groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    def create(self, validated_data):
        pass

    def update(self, teacher: Teacher, validated_data):
        user = teacher.user
        user.is_active = True
        if groups := validated_data.pop("permission_groups", []):
            user.groups.set(groups)
        user.save()
        return teacher
