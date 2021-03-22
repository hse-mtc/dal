from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ImageField,
    PrimaryKeyRelatedField,
    CharField,
)

from drf_writable_nested.serializers import WritableNestedModelSerializer

from common.models.persons import Photo
from common.serializers.persons import (
    RelativeSerializer,
    PersonnelMutateSerializer,
)

from lms.models.common import Milgroup
from lms.models.universities import Program
from lms.models.students import (
    Student,
    Passport,
    RecruitmentOffice,
    UniversityInfo,
)
from lms.serializers.common import MilgroupSerializer


class ProgramSerializer(ModelSerializer):

    class Meta:
        model = Program
        fields = "__all__"
        extra_kwargs = {"code": {"validators": []}}


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


class PassportSerializer(ModelSerializer):

    class Meta:
        model = Passport
        exclude = ["id"]


class RecruitmentOfficeSerializer(ModelSerializer):

    class Meta:
        model = RecruitmentOffice
        exclude = ["id"]


class UniversityInfoSerializer(ModelSerializer):
    program = CharField(max_length=8)

    def create(self, validated_data):
        code = validated_data.pop("program")
        query = Program.objects.filter(code=code)

        if not query.exists():
            Program.objects.create(code=code)
        validated_data["program"] = query.first()

        return super().create(validated_data)

    class Meta:
        model = UniversityInfo
        exclude = ["id"]


class StudentSerializer(WritableNestedModelSerializer):
    milgroup = MilgroupSerializer()
    program = ProgramSerializer()
    photo = PhotoSerializer(read_only=True)

    fullname = SerializerMethodField()

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
    family = RelativeSerializer(required=False, many=True)
    recruitment_office = RecruitmentOfficeSerializer(required=False)
    university_info = UniversityInfoSerializer(required=False)

    class Meta(PersonnelMutateSerializer.Meta):
        model = Student

    def create(self, validated_data):
        self.create_photo(validated_data)
        return super().create(validated_data)

    def update(self, instance: Student, validated_data):
        self.update_photo(instance, validated_data)
        return super().update(instance, validated_data)


class StudentShortSerializer(ModelSerializer):
    fullname = SerializerMethodField(required=False)
    milgroup = MilgroupSerializer(required=False)

    def get_fullname(self, obj):
        return f"{obj.surname} {obj.name} {obj.patronymic}"

    class Meta:
        model = Student
        fields = ["id", "fullname", "milgroup"]
