from rest_framework.serializers import (Serializer, ModelSerializer,
                                        IntegerField, DateField,
                                        SerializerMethodField)
from rest_framework.serializers import ValidationError
from drf_writable_nested.serializers import WritableNestedModelSerializer

from lms.models.absence import Absence
from lms.models.student import Student
from lms.models.common import Milgroup

from lms.validators import PresentInDatabaseValidator
from lms.serializers.student import StudentShortSerializer


class AbsenceSerializer(WritableNestedModelSerializer):
    student = StudentShortSerializer(
        required=False, validators=[PresentInDatabaseValidator(Student)])

    class Meta:
        model = Absence
        fields = '__all__'


class AbsenceJournalGetQuerySerializer(Serializer):
    milgroup = IntegerField(
        required=True,
        validators=[PresentInDatabaseValidator(Milgroup, 'milgroup')])
    date_from = DateField(required=False)
    date_to = DateField(required=False)

    def validate(self, attrs):
        if attrs['date_from'] > attrs['date_to']:
            raise ValidationError(
                'date_from should be greater or equal to date_to')
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class AbsenceShortSerializer(ModelSerializer):

    class Meta:
        model = Absence
        fields = [
            'id', 'date', 'absence_type', 'absence_status', 'reason', 'comment'
        ]


class AbsenceJournalSerializer(ModelSerializer):
    fullname = SerializerMethodField(read_only=True)
    absences = SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'fullname', 'absences']

    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    def get_absences(self, obj):
        absences = obj.absence_set.filter(date__in=self.context['date_range'])
        return AbsenceShortSerializer(absences, many=True).data
