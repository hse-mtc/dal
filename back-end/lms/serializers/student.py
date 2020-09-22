from rest_framework.serializers import (ModelSerializer, Serializer,
                                        IntegerField, CharField, DateField,
                                        SerializerMethodField)
from rest_framework.serializers import ValidationError

from lms.models import (
    Milfaculty,
    Milgroup,
    Status,
    Program,
    Student,
)

from lms.validators import PresentInDatasetValidator
from lms.serializers.serializers import MilgroupSerializer, ProgramSerializer


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


class StudentSerializer(ModelSerializer):
    milgroup = MilgroupSerializer(required=False,
        many=False, validators=[PresentInDatasetValidator(Milgroup)])
    program = ProgramSerializer(required=False, many=False,
                                validators=[PresentInDatasetValidator(Program)])
    status = CharField(required=False, 
                       validators=[PresentInDatasetValidator(Status, 'status')])

    birthdate = DateField(required=False, format='%d.%m.%Y',
                          input_formats=['%d.%m.%Y', 'iso-8601'])

    name = CharField(required=False)
    fullname = SerializerMethodField(required=False)

    class Meta:
        model = Student
        fields = '__all__'

    # pylint: disable=no-self-use
    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    # pylint: disable=too-many-locals
    def create(self, validated_data):
        milgroup_data = validated_data.pop('milgroup')
        milfaculty = Milfaculty.objects.get(
            milfaculty=milgroup_data.pop('milfaculty'))
        milgroup = Milgroup.objects.get(milfaculty=milfaculty, **milgroup_data)

        program = Program.objects.get(**validated_data.pop('program'))

        status = Status.objects.get(status=validated_data.pop('status'))

        return Student.objects.create(milgroup=milgroup,
                                             program=program,
                                             status=status,
                                             **validated_data)


    # pylint: disable=too-many-locals
    def update(self, instance, validated_data):
        milgroup_data = validated_data.pop('milgroup')
        milfaculty = Milfaculty.objects.get(
            milfaculty=milgroup_data.pop('milfaculty'))
        milgroup = Milgroup.objects.get(milfaculty=milfaculty, **milgroup_data)

        program = Program.objects.get(**validated_data.pop('program'))

        # serializer converts
        return instance.update(milgroup=milgroup,
                                           program=program,
                                           **validated_data)


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