from rest_framework.serializers import (ModelSerializer, Serializer,
                                        IntegerField, CharField, DateField)
from rest_framework.serializers import ValidationError

from lms.models import (
    Absence,
    Student,
    AbsenceType,
    AbsenceStatus,
    Milgroup,
)

from lms.validators import PresentInDatasetValidator
from lms.serializers.student import StudentShortSerializer


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

        return Absence.objects.create(absenceType=absence_type,
                                             absenceStatus=absence_status,
                                             studentid=student,
                                             **validated_data)
