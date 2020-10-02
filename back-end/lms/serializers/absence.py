from rest_framework.serializers import (Serializer, ModelSerializer,
                                        IntegerField, CharField,
                                        SerializerMethodField)

from lms.models import (
    Absence,
    Student,
    AbsenceType,
    AbsenceStatus,
    Milgroup,
)

from lms.validators import PresentInDatabaseValidator
from lms.serializers.student import StudentShortSerializer
from lms.serializers.serializers import NestedModelSerializer


class AbsenceSerializer(NestedModelSerializer):
    absenceType = CharField(
        required=False,
        validators=[PresentInDatabaseValidator(AbsenceType, 'absenceType')])
    absenceStatus = CharField(
        required=False,
        validators=[PresentInDatabaseValidator(AbsenceStatus, 'absenceStatus')])
    studentid = StudentShortSerializer(
        required=False, validators=[PresentInDatabaseValidator(Student)])

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
        validators=[PresentInDatabaseValidator(Milgroup, 'milgroup')])

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class AbsenceShortSerializer(ModelSerializer):

    class Meta:
        model = Absence
        fields = [
            'id', 'date', 'absenceType', 'absenceStatus', 'reason', 'comment'
        ]


class AbsenceJournalSerializer(ModelSerializer):
    fullname = SerializerMethodField(read_only=True)
    absences = SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'fullname', 'absences']

    def get_fullname(self, obj):
        # pylint: disable=no-self-use
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    def get_absences(self, obj):
        absences = obj.absence_set.filter(date__in=self.context['date_range'])
        return AbsenceShortSerializer(absences, many=True).data
