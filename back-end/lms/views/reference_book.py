from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

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


class ReferenceBookView(ListAPIView):
    permission_classes = [AllowAny]

    model_serializer = {
        'milgroups': (Milgroup, MilgroupSerializer),
        'program': (Program, ProgramSerializer),
        'ranks': (Rank, RankSerializer),
        'skills': (Skill, SkillSerializer),
        'teacher_posts': (TeacherPost, TeacherPostSerializer),
        'student_posts': (StudentPost, StudentPostSerializer)
    }

    def list(self, request, *args, **kwargs):
        # pylint:disable=(too-many-locals)
        response = {}
        for title in self.model_serializer:
            model, serializer = self.model_serializer[title]
            response_to_add = {
                title: serializer(model.objects.all(), many=True).data
            }
            response.update(response_to_add)

        return Response(response)
