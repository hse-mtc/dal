from rest_framework.serializers import (Serializer, ModelSerializer, 
                                        SerializerMethodField, CharField,
                                        IntegerField)

from lms.models import (
    Milfaculty,
    Milgroup,
    Rank,
    TeacherPost,
    Teacher,
)

from lms.validators import PresentInDatasetValidator
from lms.serializers.serializers import MilgroupSerializer


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


class TeacherSerializer(ModelSerializer):
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

    # pylint: disable=(no-self-use)
    def create(self, validated_data):
        milgroup = Milgroup.objects.get(**validated_data.pop('milgroup'))
        milfaculty = Milfaculty.objects.get(milfaculty=validated_data.pop('milfaculty'))
        rank = Rank.objects.get(rank=validated_data.pop('rank'))
        teacherPost = TeacherPost.objects.get(teacherPost=validated_data.pop('teacherPost'))

        return Teacher.objects.create(milgroup=milgroup,
                                             milfaculty=milfaculty,
                                             rank=rank,
                                             teacherPost=teacherPost,
                                             **validated_data)

    def update(self, instance, validated_data):
        if 'milgroup' in validated_data:
            milgroup = Milgroup.objects.get(**validated_data.pop('milgroup'))
            instance.milgroup = milgroup

        if 'milfaculty' in validated_data:
            milfaculty = Milfaculty.objects.get(milfaculty=validated_data.pop('milfaculty'))
            instance.milfaculty = milfaculty

        if 'rank' in validated_data:
            rank = Rank.objects.get(rank=validated_data.pop('rank'))
            instance.rank = rank
        
        if 'teacherPost' in validated_data:
            teacherPost = TeacherPost.objects.get(teacherPost=validated_data.pop('teacherPost'))
            instance.teacherPost = teacherPost

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        return instance
