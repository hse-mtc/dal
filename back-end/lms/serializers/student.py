from rest_framework.serializers import (Serializer, IntegerField, CharField,
                                        DateField, SerializerMethodField)
from rest_framework.serializers import ValidationError


from lms.models import (
    Milgroup,
    Status,
    Program,
    Student,
)
from lms.validators import PresentInDatabaseValidator
from lms.serializers.serializers import (NestedModelSerializer,
                                         MilgroupSerializer, ProgramSerializer)


class StudentSerializer(NestedModelSerializer):
    milgroup = MilgroupSerializer(required=False,
            validators=[PresentInDatabaseValidator(Milgroup)])
    program = ProgramSerializer(required=False,
            validators=[PresentInDatabaseValidator(Program)])
    status = CharField(required=False,
            validators=[PresentInDatabaseValidator(Status, 'status')])

    fullname = SerializerMethodField(required=False)

    class Meta:
        model = Student
        fields = '__all__'

    def get_fullname(self, obj):
        # pylint: disable=no-self-use
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    nested_fields = [
        ['milgroup', Milgroup],
        ['program', Program],
        ['status', Status, 'status'],
    ]


class StudentShortSerializer(NestedModelSerializer):
    fullname = SerializerMethodField(required=False)
    milgroup = MilgroupSerializer(many=False, required=False,
            validators=[PresentInDatabaseValidator(Milgroup)])

    # pylint: disable=no-self-use
    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    class Meta:
        model = Student
        fields = ['id', 'fullname', 'milgroup']

    nested_fields = [['milgroup', Milgroup]]
