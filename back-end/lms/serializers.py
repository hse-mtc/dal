import datetime

from rest_framework.serializers import (ModelSerializer, Serializer,
                                        IntegerField, CharField, DateField,
                                        SerializerMethodField)
from rest_framework.serializers import ValidationError

from .models import (
    Milfaculty,
    Milgroup,
    Program,
    Student,
    Teacher,
    Status,
    Absence,
    AbsenceType,
    AbsenceStatus,
)

from .validators import PresentInDatasetValidator


class MilgroupSerializer(ModelSerializer):
    milgroup = IntegerField()

    class Meta:
        model = Milgroup
        fields = '__all__'


class ProgramSerializer(ModelSerializer):

    class Meta:
        model = Program
        fields = '__all__'
        extra_kwargs = {'code': {'validators': []}}


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
    milgroup = MilgroupSerializer(
        many=False, validators=[PresentInDatasetValidator(Milgroup)])
    program = ProgramSerializer(many=False,
                                validators=[PresentInDatasetValidator(Program)])
    status = CharField(validators=[PresentInDatasetValidator(Status, 'status')])

    birthdate = DateField(format='%d.%m.%Y',
                          input_formats=['%d.%m.%Y', 'iso-8601'])

    fullname = SerializerMethodField()

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

        student_new = Student.objects.create(milgroup=milgroup,
                                             program=program,
                                             status=status,
                                             **validated_data)

        return student_new

    # pylint: disable=too-many-locals
    def update(self, instance, validated_data):
        milgroup_data = validated_data.pop('milgroup')
        milfaculty = Milfaculty.objects.get(
            milfaculty=milgroup_data.pop('milfaculty'))
        milgroup = Milgroup.objects.get(milfaculty=milfaculty, **milgroup_data)

        program = Program.objects.get(**validated_data.pop('program'))

        # Convert from '%d.%m.%Y' format to '%Y-%m-%d' format
        # because Django doesn't accept russian formats.
        # Though, it accepts russian format on creating -_-
        validated_data['birthdate'] = datetime.datetime.strptime(
            validated_data['birthdate'], '%d.%m.%Y').strftime('%Y-%m-%d')
        # serializer converts
        student_modified = instance.update(milgroup=milgroup,
                                           program=program,
                                           **validated_data)

        return student_modified


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


class AbsenceGetQuerySerializer(Serializer):
    id = IntegerField(min_value=1,
                      required=False,
                      validators=[PresentInDatasetValidator(Absence, 'id')])
    studentid = IntegerField(
        min_value=1,
        required=False,
        validators=[PresentInDatasetValidator(Student, 'id')])
    name = CharField(required=False)
    absenceType = CharField(
        required=False,
        validators=[PresentInDatasetValidator(AbsenceType, 'absenceType')])
    date_from = DateField(required=False,
                          format='%d.%m.%Y',
                          input_formats=['%d.%m.%Y', 'iso-8601'])
    date_to = DateField(required=False,
                        format='%d.%m.%Y',
                        input_formats=['%d.%m.%Y', 'iso-8601'])
    absenceStatus = CharField(
        required=False,
        validators=[PresentInDatasetValidator(AbsenceStatus, 'absenceStatus')])
    milgroup = IntegerField(
        required=False,
        validators=[PresentInDatasetValidator(Milgroup, 'milgroup')])

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


class AbsenceSerializer(ModelSerializer):
    date = DateField(format='%d.%m.%Y', input_formats=['%d.%m.%Y', 'iso-8601'])

    absenceType = CharField(
        validators=[PresentInDatasetValidator(AbsenceType, 'absenceType')])
    absenceStatus = CharField(
        validators=[PresentInDatasetValidator(AbsenceStatus, 'absenceStatus')])
    studentid = StudentShortSerializer(
        validators=[PresentInDatasetValidator(Student)])

    class Meta:
        model = Absence
        fields = '__all__'

    def create(self, validated_data):
        absence_type = AbsenceType.objects.get(
            absenceType=validated_data.pop('absenceType'))
        absence_status = AbsenceStatus.objects.get(
            absenceStatus=validated_data.pop('absenceStatus'))

        student = Student.objects.get(**validated_data.pop('studentid'))

        absence_new = Absence.objects.create(absenceType=absence_type,
                                             absenceStatus=absence_status,
                                             studentid=student,
                                             **validated_data)

        return absence_new


class TeacherSerializer(ModelSerializer):
    milgroup = MilgroupSerializer(many=False)
    fullname = SerializerMethodField()

    class Meta:
        model = Teacher
        fields = '__all__'

    # pylint: disable=(no-self-use)
    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    # pylint: disable=(no-self-use)
    def create(self, validated_data):
        milgroup_data = validated_data.pop('milgroup')
        milfaculty = Milfaculty.objects.get(
            milfaculty=validated_data.pop('milgroup'))
        milgroup = Milgroup.objects.get(milfaculty=milfaculty, **milgroup_data)

        new_teacher = Teacher.objects.create(milgroup=milgroup,
                                             **validated_data)
        return new_teacher

    def update(self, instance, validated_data):
        milgroup_data = validated_data.pop('milgroup')
        milfaculty = Milfaculty.objects.get(
            milfaculty=milgroup_data.pop('milfaculty'))
        milgroup = Milgroup.objects.get(milfaculty=milfaculty, **milgroup_data)

        teacher_modified = instance.update(milgroup=milgroup, **validated_data)
        return teacher_modified
