from rest_framework.serializers import (Serializer, IntegerField, 
                                        CharField, DateField)
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
from lms.serializers.serializers import NestedModelSerializer


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


class AbsenceSerializer(NestedModelSerializer):
    date = DateField(required=False,
                format='%d.%m.%Y', input_formats=['%d.%m.%Y', 'iso-8601'])

    absenceType = CharField(required=False,
        validators=[PresentInDatasetValidator(AbsenceType, 'absenceType')])
    absenceStatus = CharField(required=False,
        validators=[PresentInDatasetValidator(AbsenceStatus, 'absenceStatus')])
    studentid = StudentShortSerializer(required=False,
        validators=[PresentInDatasetValidator(Student)])

    class Meta:
        model = Absence
        fields = '__all__'

    nested_fields = [
        ['absenceType', AbsenceType, 'absenceType'],
        ['absenceStatus', AbsenceStatus, 'absenceStatus'],
        ['studentid', Student],
    ]


class AbsenceJournalGetQuerySerializer(Serializer):
    milgroup = IntegerField(required=True,
                validators=[PresentInDatasetValidator(Milgroup, 'milgroup')])
    date_from = DateField(required=True,
                          format='%d.%m.%Y',
                          input_formats=['%d.%m.%Y'])
    date_to = DateField(required=True,
                          format='%d.%m.%Y',
                          input_formats=['%d.%m.%Y'])
