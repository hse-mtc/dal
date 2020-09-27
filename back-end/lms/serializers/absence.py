from rest_framework.serializers import (Serializer, ModelSerializer, 
                                        IntegerField, CharField,
                                        DateField, SerializerMethodField)
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
from lms.serializers.serializers import (NestedModelSerializer, 
                                         MilgroupSerializer)


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
                     format='%d.%m.%Y',
                     input_formats=['%d.%m.%Y', 'iso-8601'])

    absenceType = CharField(
        required=False,
        validators=[PresentInDatasetValidator(AbsenceType, 'absenceType')])
    absenceStatus = CharField(
        required=False,
        validators=[PresentInDatasetValidator(AbsenceStatus, 'absenceStatus')])
    studentid = StudentShortSerializer(
        required=False, validators=[PresentInDatasetValidator(Student)])

    class Meta:
        model = Absence
        fields = '__all__'

    nested_fields = [
        ['absenceType', AbsenceType, 'absenceType'],
        ['absenceStatus', AbsenceStatus, 'absenceStatus'],
        ['studentid', Student],
    ]


class AbsenceJournalGetQuerySerializer(Serializer):
    milgroup = IntegerField(
        required=True,
        validators=[PresentInDatasetValidator(Milgroup, 'milgroup')])
    date_from = DateField(required=True,
                          format='%d.%m.%Y',
                          input_formats=['%d.%m.%Y'])
    date_to = DateField(required=True,
                        format='%d.%m.%Y',
                        input_formats=['%d.%m.%Y'])

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class AbsenceShortSerializer(ModelSerializer):
    absenceType = CharField(read_only=True)
    absenceStatus = CharField(read_only=True)
    date = DateField(read_only=True, format='%d.%m.%Y')

    class Meta:
        model = Absence
        fields = ['date', 'absenceType', 'absenceStatus',
                  'reason', 'comment']


class AbsenceJournalSerializer(ModelSerializer):
    id = IntegerField(read_only=True)
    fullname = SerializerMethodField(read_only=True)
    absences = AbsenceShortSerializer(read_only=True,
                                      many=True,
                                      source='absence_set')
    
    def __init__(self, *args, **kwargs):
        date_range = kwargs.pop('date_range')
        super().__init__(*args, **kwargs)
        query_params = self.context['request'].query_params
        self.fields['absences'].queryset = Absence.objects.filter(date__in=date_range)

    class Meta:
        model = Student
        fields = ['id', 'fullname', 'absences']
    
    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'
