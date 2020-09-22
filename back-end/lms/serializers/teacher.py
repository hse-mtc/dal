from rest_framework.serializers import (Serializer, SerializerMethodField, 
                                        CharField, IntegerField)

from lms.models import (
    Milfaculty,
    Milgroup,
    Rank,
    TeacherPost,
    Teacher,
)

from lms.validators import PresentInDatasetValidator
from lms.serializers.serializers import (
    MilgroupSerializer, NestedModelSerializer)


class TeacherGetQuerySerializer(Serializer):
    id = IntegerField(min_value=1,
                      required=False,
                      validators=[PresentInDatasetValidator(Teacher, 'id')])
    milgroup = IntegerField(
        required=False,
        validators=[PresentInDatasetValidator(Milgroup, 'milgroup')])
    name = CharField(required=False)
    milfaculty = CharField(
        required=False,
        validators=[PresentInDatasetValidator(Milfaculty, 'milfaculty')])
    rank = CharField(
        required=False,
        validators=[PresentInDatasetValidator(Rank, 'rank')])
    teacherPost = CharField(
        required=False,
        validators=[PresentInDatasetValidator(TeacherPost, 'teacherPost')])


class TeacherSerializer(NestedModelSerializer):
    milgroup = MilgroupSerializer(required=False,
        many=False, validators=[PresentInDatasetValidator(Milgroup)])
    
    name = CharField(required=False)
    surname = CharField(required=False)
    patronymic = CharField(required=False)
    fullname = SerializerMethodField(required=False)

    milfaculty = CharField(
        required=False,
        validators=[PresentInDatasetValidator(Milfaculty, 'milfaculty')])
    rank = CharField(
        required=False,
        validators=[PresentInDatasetValidator(Rank, 'rank')])
    teacherPost = CharField(
        required=False,
        validators=[PresentInDatasetValidator(TeacherPost, 'teacherPost')])

    class Meta:
        model = Teacher
        fields = '__all__'

    # pylint: disable=(no-self-use)
    def get_fullname(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    nested_fields = [
        ['milgroup', Milgroup],
        ['milfaculty', Milfaculty, 'milfaculty'],
        ['rank', Rank, 'rank'],
        ['teacherPost', TeacherPost, 'teacherPost'],
    ]
