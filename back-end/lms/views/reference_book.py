from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.views import extend_schema

from lms.models.common import Milgroup, Milfaculty
from lms.models.teacher import Rank, TeacherPost
from lms.models.student import Program
from lms.models.lesson import LessonType, Room
from lms.models.absence import AbsenceType, AbsenceStatus, AbsenceTime
from lms.models.achievement import AchievementType
from lms.models.encouragement import EncouragementType
from lms.models.punishment import PunishmentType

from lms.serializers.common import MilgroupSerializer, MilfacultySerializer
from lms.serializers.student import ProgramSerializer
from lms.serializers.teacher import TeacherPostSerializer, RankSerializer
from lms.serializers.lesson import LessonTypeSerializer, RoomSerializer
from lms.serializers.absence import (AbsenceTypeSerializer,
                                     AbsenceStatusSerializer,
                                     AbsenceTimeSerializer)
from lms.serializers.achievement import AchievementTypeSerializer
from lms.serializers.encouragement import EncouragementTypeSerializer
from lms.serializers.punishment import PunishmentTypeSerializer

from lms.filters.reference_book import MilgroupFilter, ProgramFilter

from auth.permissions import BasicPermission


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
        'lesson_type': (LessonType, LessonTypeSerializer),
        'rooms': (Room, RoomSerializer),
        'absence_type': (AbsenceType, AbsenceTypeSerializer),
        'absence_status': (AbsenceStatus, AbsenceStatusSerializer),
        'absence_time': (AbsenceTime, AbsenceTimeSerializer),
        'achievement_type': (AchievementType, AchievementTypeSerializer),
        'encouragement_type': (EncouragementType, EncouragementTypeSerializer),
        'punishment_type': (PunishmentType, PunishmentTypeSerializer),
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
class MilfacultyView(ModelViewSet):
    serializer_class = MilfacultySerializer
    queryset = Milfaculty.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class MilgroupView(ModelViewSet):
    serializer_class = MilgroupSerializer
    queryset = Milgroup.objects.all()

    permission_classes = [ReferenceBookPermission]

    filterset_class = MilgroupFilter


@extend_schema(tags=['reference-book'])
class ProgramView(ModelViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()

    permission_classes = [ReferenceBookPermission]

    filterset_class = ProgramFilter


@extend_schema(tags=['reference-book'])
class RankView(ModelViewSet):
    serializer_class = RankSerializer
    queryset = Rank.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class TeacherPostView(ModelViewSet):
    serializer_class = TeacherPostSerializer
    queryset = TeacherPost.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class LessonTypeView(ModelViewSet):
    serializer_class = LessonTypeSerializer
    queryset = LessonType.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class RoomView(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class AbsenceTypeView(ModelViewSet):
    serializer_class = AbsenceTypeSerializer
    queryset = AbsenceType.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class AbsenceStatusView(ModelViewSet):
    serializer_class = AbsenceStatusSerializer
    queryset = AbsenceStatus.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class AbsenceTimeView(ModelViewSet):
    serializer_class = AbsenceTimeSerializer
    queryset = AbsenceTime.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class AchievementTypeView(ModelViewSet):
    serializer_class = AchievementTypeSerializer
    queryset = AchievementType.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class EncouragementTypeView(ModelViewSet):
    serializer_class = EncouragementTypeSerializer
    queryset = EncouragementType.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=['reference-book'])
class PunishmentTypeView(ModelViewSet):
    serializer_class = PunishmentTypeSerializer
    queryset = PunishmentType.objects.all()

    permission_classes = [ReferenceBookPermission]
