from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from lms.models import (
    TeacherPost,
    Milgroup,
    Program,
    Rank,
)

from lms.serializers.serializers import (MilgroupSerializer, ProgramSerializer,
                                         RankSerializer, TeacherPostSerializer)


class ReferenceBookView(ListAPIView):
    permission_classes = [AllowAny]

    model_serializer = {
        'milgroups': (Milgroup, MilgroupSerializer),
        'program': (Program, ProgramSerializer),
        'ranks': (Rank, RankSerializer),
        'teacher_posts': (TeacherPost, TeacherPostSerializer),
    }

    def list(self, request, *args, **kwargs):
        # pylint:disable=(too-many-locals)
        response = {}
        for title in self.model_serializer:
            model, serializer = self.model_serializer[title]
            response[title] = serializer(model.objects.all(), many=True).data

        return Response(response)
