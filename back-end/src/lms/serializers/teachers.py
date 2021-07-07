from rest_framework.serializers import (IntegerField, SerializerMethodField,
                                        ModelSerializer)
from drf_writable_nested.serializers import WritableNestedModelSerializer
from common.serializers.persons import (BirthInfoSerializer, ContactInfoSerializer, PersonnelMutateSerializer,)

from lms.models.common import Milgroup
from lms.models.teachers import Rank, TeacherPost, Teacher

from lms.validators import PresentInDatabaseValidator
from lms.serializers.common import MilgroupSerializer
from lms.serializers.students import PhotoSerializer


class RankSerializer(ModelSerializer):

    class Meta:
        model = Rank
        fields = '__all__'


class TeacherPostSerializer(ModelSerializer):

    class Meta:
        model = TeacherPost
        fields = '__all__'


class TeacherSerializer(WritableNestedModelSerializer):
    fullname = SerializerMethodField(required=False)
    milgroup = MilgroupSerializer()
    birth_info = BirthInfoSerializer()
    contact_info = ContactInfoSerializer()

    birth_info = BirthInfoSerializer()
    photo = PhotoSerializer(read_only=True)

    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherMutateSerializer(WritableNestedModelSerializer,
                              PersonnelMutateSerializer):
    birth_info = BirthInfoSerializer()
    contact_info = ContactInfoSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        self.create_photo(validated_data)
        return super().create(validated_data)

    def update(self, instance: Teacher, validated_data):
        self.update_photo(instance, validated_data)
        return super().update(instance, validated_data)


class TeacherShortSerializer(WritableNestedModelSerializer):
    id = IntegerField(required=False)
    fullname = SerializerMethodField(required=False)
    milgroup = MilgroupSerializer(
        required=False,
        many=False,
        validators=[PresentInDatabaseValidator(Milgroup)])

    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    class Meta:
        model = Teacher
        fields = ['id', 'fullname', 'milgroup']
