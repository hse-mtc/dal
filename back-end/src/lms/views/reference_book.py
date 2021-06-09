from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from lms.models.common import (
    Milfaculty,
    Milspecialty,
    Milgroup,
)
from lms.models.teachers import Rank, TeacherPost
from lms.models.lessons import Room
from lms.models.absences import AbsenceTime
from lms.models.achievements import AchievementType
from lms.models.universities import Program
from lms.models.students import StudentPost, StudentSkill

from lms.serializers.common import (
    MilfacultySerializer,
    MilspecialtySerializer,
    MilgroupSerializer,
)
from lms.serializers.universities import ProgramSerializer
from lms.serializers.teachers import TeacherPostSerializer, RankSerializer
from lms.serializers.lessons import RoomSerializer
from lms.serializers.absences import AbsenceTimeSerializer
from lms.serializers.achievements import AchievementTypeSerializer
from lms.serializers.students import (
    StudentPostSerializer,
    StudentSkillSerializer,
)

from lms.filters.reference_books import (
    MilspecialtyFilter,
    MilgroupFilter,
    ProgramFilter,
)

from auth.permissions import (
    BasePermission,
    ReadOnly,
)


class ReferenceBookPermission(BasePermission):
    permission_class = 'reference_book'


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
        'student_post': (StudentPost, StudentPostSerializer)
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

    filter_backends = [DjangoFilterBackend]
    filterset_class = MilspecialtyFilter


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


@extend_schema(tags=['reference-book'])
class StudentPostViewSet(ModelViewSet):
    serializer_class = StudentPostSerializer
    queryset = StudentPost.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class StudentSkillViewSet(ModelViewSet):
    serializer_class = StudentSkillSerializer
    queryset = StudentSkill.objects.all()

    permission_classes = [ReferenceBookPermission]
