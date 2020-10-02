from rest_framework.serializers import SerializerMethodField, CharField

from lms.models import (
    Milfaculty,
    Milgroup,
    Rank,
    TeacherPost,
    Teacher,
)

from lms.validators import PresentInDatabaseValidator
from lms.serializers.serializers import (MilgroupSerializer,
                                         NestedModelSerializer)


class TeacherSerializer(NestedModelSerializer):
    milgroup = MilgroupSerializer(
        required=False,
        many=False,
        validators=[PresentInDatabaseValidator(Milgroup)])
    milfaculty = CharField(
        required=False,
        validators=[PresentInDatabaseValidator(Milfaculty, 'milfaculty')])
    rank = CharField(required=False,
                     validators=[PresentInDatabaseValidator(Rank, 'rank')])
    teacher_post = CharField(
        required=False,
        validators=[PresentInDatabaseValidator(TeacherPost, 'teacher_post')])

    fullname = SerializerMethodField(required=False)

    class Meta:
        model = Teacher
        fields = '__all__'

    def get_fullname(self, obj):
        # pylint: disable=(no-self-use)
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    nested_fields = [
        ['milgroup', Milgroup],
        ['milfaculty', Milfaculty, 'milfaculty'],
        ['rank', Rank, 'rank'],
        ['teacher_post', TeacherPost, 'teacher_post'],
    ]
