from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_spectacular.views import extend_schema

from lms.models.common import Milgroup
from lms.models.teacher import Rank, TeacherPost
from lms.models.student import Program
from lms.models.lesson import Room

from lms.serializers.common import MilgroupSerializer
from lms.serializers.student import ProgramSerializer
from lms.serializers.teacher import TeacherPostSerializer, RankSerializer
from lms.serializers.lesson import RoomSerializer


@extend_schema(tags=['reference-book'])
class ReferenceBookView(ListAPIView):
    permission_classes = [AllowAny]

    model_serializer = {
        'milgroups': (Milgroup, MilgroupSerializer),
        'program': (Program, ProgramSerializer),
        'ranks': (Rank, RankSerializer),
        'teacher_posts': (TeacherPost, TeacherPostSerializer),
        'rooms': (Room, RoomSerializer),
    }

    def list(self, request, *args, **kwargs):
        # pylint:disable=(too-many-locals)
        if request.data:
            titles = request.data['filter_by']
        else:
            titles = self.model_serializer.keys()
        response = {}
        for title in titles:
            model, serializer = self.model_serializer[title]
            response[title] = serializer(model.objects.all(), many=True).data

        return Response(response)
