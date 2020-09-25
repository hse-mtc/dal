from rest_framework.serializers import (ModelSerializer, Serializer,
                                        IntegerField, CharField, DateField,
                                        SerializerMethodField)
from rest_framework.serializers import ValidationError

from lms.models import (
    Milgroup,
    Status,
    Program,
    Student,
)

from lms.validators import PresentInDatasetValidator
from lms.serializers.serializers import (NestedModelSerializer,
                                         MilgroupSerializer, ProgramSerializer)


class StudentGetQuerySerializer(Serializer):
    id = IntegerField(min_value=1,
                      required=False,
                      validators=[PresentInDatasetValidator(Student, 'id')])
    milgroup = IntegerField(
        required=False,
        validators=[PresentInDatasetValidator(Milgroup, 'milgroup')])
    name = CharField(required=False)
    status = CharField(required=False,
                       validators=[PresentInDatasetValidator(Status, 'status')])

    def validate(self, attrs):
        if 'id' in attrs and len(attrs) > 1:
            raise ValidationError(
                'If id is given, all other searching keys will be ignored '
                'and therefore should be deleted')
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class StudentSerializer(NestedModelSerializer):
    milgroup = MilgroupSerializer(
        required=False,
        many=False,
        validators=[PresentInDatasetValidator(Milgroup)])
    program = ProgramSerializer(required=False,
                                many=False,
                                validators=[PresentInDatasetValidator(Program)])
    status = CharField(required=False,
                       validators=[PresentInDatasetValidator(Status, 'status')])

    birthdate = DateField(required=False,
                          format='%d.%m.%Y',
                          input_formats=['%d.%m.%Y', 'iso-8601'])

    name = CharField(required=False)
    surname = CharField(required=False)
    patronymic = CharField(required=False)
    fullname = SerializerMethodField(required=False)

    class Meta:
        model = Student
        fields = '__all__'

    # pylint: disable=no-self-use
    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    nested_fields = [
        ['milgroup', Milgroup],
        ['program', Program],
        ['status', Status, 'status'],
    ]


class StudentShortSerializer(ModelSerializer):
    fullname = SerializerMethodField()
    milgroup = MilgroupSerializer(
        many=False,
        required=False,
        validators=[PresentInDatasetValidator(Milgroup)])

    # pylint: disable=no-self-use
    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    class Meta:
        model = Student
        fields = ['id', 'name', 'surname', 'patronymic', 'fullname', 'milgroup']

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
