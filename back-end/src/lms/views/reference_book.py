from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.views import extend_schema

from lms.models.common import (
    Milfaculty,
    Milspecialty,
    Milgroup,
)
from lms.models.teachers import Rank, TeacherPost
from lms.models.universities import Program
from lms.models.lessons import Room
from lms.models.absences import AbsenceTime
from lms.models.achievements import AchievementType

from lms.serializers.common import (
    MilfacultySerializer,
    MilspecialtySerializer,
    MilgroupSerializer,
)
from lms.serializers.students import ProgramSerializer
from lms.serializers.teachers import TeacherPostSerializer, RankSerializer
from lms.serializers.lessons import RoomSerializer
from lms.serializers.absences import AbsenceTimeSerializer
from lms.serializers.achievements import AchievementTypeSerializer

from lms.filters.reference_books import MilgroupFilter, ProgramFilter

from auth.permissions import (
    BasicPermission,
    ReadOnly,
)


class ReferenceBookPermission(BasicPermission):
    permission_class = 'auth.reference_book'


@extend_schema(tags=['reference-book'])
class ReferenceBookView(ListAPIView):
    permission_classes = [ReferenceBookPermission]

    model_serializer = {
        'milfaculties': (Milfaculty, MilfacultySerializer),
        'milgroups': (Milgroup, MilgroupSerializer),
        'program': (Program, ProgramSerializer),
        'ranks': (Rank, RankSerializer),
        'teacher_posts': (TeacherPost, TeacherPostSerializer),
        'rooms': (Room, RoomSerializer),
        'absence_time': (AbsenceTime, AbsenceTimeSerializer),
        'achievement_type': (AchievementType, AchievementTypeSerializer),
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


@extend_schema(tags=['reference-book'])
class MilfacultyViewSet(ModelViewSet):
    serializer_class = MilfacultySerializer
    queryset = Milfaculty.objects.all()

    permission_classes = [ReadOnly | ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class MilspecialtyViewSet(ModelViewSet):
    serializer_class = MilspecialtySerializer
    queryset = Milspecialty.objects.all()

    permission_classes = [ReadOnly | ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class MilgroupViewSet(ModelViewSet):
    serializer_class = MilgroupSerializer
    queryset = Milgroup.objects.all()

    permission_classes = [ReadOnly | ReferenceBookPermission]

    filterset_class = MilgroupFilter


@extend_schema(tags=['reference-book'])
class ProgramViewSet(ModelViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()

    permission_classes = [ReadOnly | ReferenceBookPermission]

    filterset_class = ProgramFilter


@extend_schema(tags=['reference-book'])
class RankViewSet(ModelViewSet):
    serializer_class = RankSerializer
    queryset = Rank.objects.all()

    permission_classes = [ReadOnly | ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class TeacherPostViewSet(ModelViewSet):
    serializer_class = TeacherPostSerializer
    queryset = TeacherPost.objects.all()

    permission_classes = [ReadOnly | ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class AbsenceTimeViewSet(ModelViewSet):
    serializer_class = AbsenceTimeSerializer
    queryset = AbsenceTime.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class AchievementTypeViewSet(ModelViewSet):
    serializer_class = AchievementTypeSerializer
    queryset = AchievementType.objects.all()

    permission_classes = [ReferenceBookPermission]
