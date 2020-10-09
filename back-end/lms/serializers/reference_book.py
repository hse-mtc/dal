from rest_framework.serializers import (Serializer, SerializerMethodField)

from lms.models import (
    StudentPost,
    TeacherPost,
    Milgroup,
    Program,
    Skill,
    Rank,
)

from lms.serializers.serializers import (MilgroupSerializer, ProgramSerializer,
                                         RankSerializer, SkillSerializer,
                                         TeacherPostSerializer,
                                         StudentPostSerializer)


class ReferenceBookSerializer(Serializer):
    milgroups = SerializerMethodField(read_only=True)
    programs = SerializerMethodField(read_only=True)
    ranks = SerializerMethodField(read_only=True)
    skills = SerializerMethodField(read_only=True)
    teacher_posts = SerializerMethodField(read_only=True)
    student_posts = SerializerMethodField(read_only=True)

    def get_milgroups(self, obj):
        # pylint: disable=unused-argument
        # pylint: disable=no-self-use
        queryset = Milgroup.objects.all()
        return MilgroupSerializer(queryset, many=True).data

    def get_programs(self, obj):
        # pylint: disable=unused-argument
        # pylint: disable=no-self-use
        queryset = Program.objects.all()
        return ProgramSerializer(queryset, many=True).data

    def get_ranks(self, obj):
        # pylint: disable=unused-argument
        # pylint: disable=no-self-use
        queryset = Rank.objects.all()
        return RankSerializer(queryset, many=True).data

    def get_skills(self, obj):
        # pylint: disable=unused-argument
        # pylint: disable=no-self-use
        queryset = Skill.objects.all()
        return SkillSerializer(queryset, many=True).data

    def get_teacher_posts(self, obj):
        # pylint: disable=unused-argument
        # pylint: disable=no-self-use
        queryset = TeacherPost.objects.all()
        return TeacherPostSerializer(queryset, many=True).data

    def get_student_posts(self, obj):
        # pylint: disable=unused-argument
        # pylint: disable=no-self-use
        queryset = StudentPost.objects.all()
        return StudentPostSerializer(queryset, many=True).data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
