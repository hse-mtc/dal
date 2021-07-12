from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
)

from drf_writable_nested.serializers import WritableNestedModelSerializer

from common.serializers.persons import (
    BirthInfoSerializer,
    ContactInfoSerializer,
    PersonnelMutateSerializer,
)

from lms.models.common import Milgroup
from lms.models.teachers import (
    Rank,
    Teacher,
)

from lms.validators import PresentInDatabaseValidator
from lms.serializers.students import PhotoSerializer
from lms.serializers.common import (
    MilgroupSerializer,
    MilfacultySerializer,
)


class RankSerializer(ModelSerializer):

    class Meta:
        model = Rank
        fields = "__all__"


class TeacherSerializer(ModelSerializer):
    fullname = SerializerMethodField(read_only=True)
    milgroups = MilgroupSerializer(read_only=True, many=True)
    milfaculty = MilfacultySerializer(read_only=True)
    rank = RankSerializer(read_only=True)
    birth_info = BirthInfoSerializer(read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)
    photo = PhotoSerializer(read_only=True)

    def get_fullname(self, obj):
        return f"{obj.surname} {obj.name} {obj.patronymic}"

    class Meta:
        model = Teacher
        fields = "__all__"


class TeacherMutateSerializer(
        WritableNestedModelSerializer,
        PersonnelMutateSerializer,
):
    birth_info = BirthInfoSerializer()
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


class TeacherShortSerializer(ModelSerializer):
    fullname = SerializerMethodField(read_only=True)
    milgroups = MilgroupSerializer(
        read_only=True,
        many=True,
        validators=[PresentInDatabaseValidator(Milgroup)],
    )

    def get_fullname(self, obj):
        return f"{obj.surname} {obj.name} {obj.patronymic}"

    class Meta:
        model = Teacher
        fields = ["id", "fullname", "milgroups"]
