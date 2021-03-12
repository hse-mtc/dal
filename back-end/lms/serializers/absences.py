from drf_writable_nested import WritableNestedModelSerializer

from rest_framework.serializers import (Serializer, ModelSerializer,
                                        IntegerField, DateField,
                                        SerializerMethodField)
from rest_framework.serializers import ValidationError
from common.serializers.populate import BaseMutateSerializer

from lms.models.absences import Absence, AbsenceTime
from lms.models.students import Student
from lms.models.common import Milgroup

from lms.validators import PresentInDatabaseValidator
from lms.serializers.students import StudentShortSerializer


class AbsenceSerializer(WritableNestedModelSerializer):
    student = StudentShortSerializer()

    class Meta:
        model = Absence
        fields = '__all__'


class AbsenceMutateSerializer(BaseMutateSerializer):

    class Meta:
        model = Absence
        fields = '__all__'


class AbsenceJournalQuerySerializer(Serializer):
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


class AbsenceTimeSerializer(ModelSerializer):

    class Meta:
        model = AbsenceTime
        fields = '__all__'
