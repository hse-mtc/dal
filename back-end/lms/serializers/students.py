from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ImageField,
)

from drf_writable_nested.serializers import WritableNestedModelSerializer

from common.models.persons import (
    PersonPhoto,
    Relative,
)
from common.serializers.populate import BaseMutateSerializer

from lms.models.students import (
    Program,
    Student,
    Passport,
    Family,
    RecruitmentOffice,
    UniversityInfo,
)
from lms.serializers.common import MilgroupSerializer


class ProgramSerializer(ModelSerializer):

    class Meta:
        model = Program
        fields = '__all__'
        extra_kwargs = {'code': {'validators': []}}


class PersonPhotoSerializer(ModelSerializer):
    image = ImageField(use_url=True,
                       allow_null=True,
                       required=False,
                       read_only=True)

    class Meta:
        model = PersonPhoto
        exclude = ['id']


class PassportSerializer(ModelSerializer):

    class Meta:
        model = Passport
        exclude = ['id']


class RelativeSerializer(ModelSerializer):

    class Meta:
        model = Relative
        exclude = ['id']


class FamilySerializer(ModelSerializer):
    mother = RelativeSerializer()
    father = RelativeSerializer()
    brothers = RelativeSerializer(many=True)
    sisters = RelativeSerializer(many=True)

    class Meta:
        model = Family
        exclude = ['id']


class RecruitmentOfficeSerializer(ModelSerializer):

    class Meta:
        model = RecruitmentOffice
        exclude = ['id']


class UniversityInfoSerializer(ModelSerializer):

    class Meta:
        model = UniversityInfo
        exclude = ['id']


class StudentSerializer(WritableNestedModelSerializer):
    milgroup = MilgroupSerializer()
    program = ProgramSerializer()
    photo = PersonPhotoSerializer(read_only=True)

    fullname = SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'

    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'


class StudentMutateSerializer(BaseMutateSerializer):
    image = ImageField(write_only=True, required=False)
    recruitment_office = RecruitmentOfficeSerializer(required=False)
    university_info = UniversityInfoSerializer(required=False)
    passport = PassportSerializer(required=False)
    family = FamilySerializer(required=False)

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        if image := validated_data.pop('image', None):
            person_photo = PersonPhoto.objects.create(image=image)
            validated_data['photo'] = person_photo
        return super().create(validated_data)

    def update(self, instance: Student, validated_data):
        if image := validated_data.pop('image', None):
            if instance.photo:
                instance.photo.image = image
                instance.photo.save()
            else:
                instance.photo = PersonPhoto.objects.create(image=image)
        return super().update(instance, validated_data)


class StudentShortSerializer(WritableNestedModelSerializer):
    fullname = SerializerMethodField(required=False)
    milgroup = MilgroupSerializer(many=False, required=False)

    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    class Meta:
        model = Student
        fields = ['id', 'fullname', 'milgroup']
