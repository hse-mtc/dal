from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema, OpenApiParameter

from lms.models.common import (
    Milfaculty,
    Milspecialty,
    Milgroup,
)
from lms.models.teachers import Rank
from lms.models.students import Student
from lms.models.lessons import Room
from lms.models.absences import AbsenceTime
from lms.models.achievements import AchievementType
from lms.models.universities import Program
from lms.models.students import Skill

from lms.serializers.common import (
    MilfacultySerializer,
    MilspecialtySerializer,
    MilgroupSerializer,
    MilgroupMutateSerializer,
    MilgroupLeadersPhonesSerializer,
)
from lms.serializers.universities import ProgramSerializer
from lms.serializers.teachers import RankSerializer
from lms.serializers.lessons import RoomSerializer
from lms.serializers.absences import AbsenceTimeSerializer
from lms.serializers.achievements import AchievementTypeSerializer
from lms.serializers.students import SkillSerializer

from lms.filters.reference_books import (
    MilspecialtyFilter,
    MilgroupFilter,
    ProgramFilter,
)

from common.constants import MUTATE_ACTIONS

from auth.permissions import (
    BasePermission,
    ReadOnly,
)


class ReferenceBookPermission(BasePermission):
    permission_class = "reference-books"
    view_name_rus = "Справочные данные"


@extend_schema(tags=["reference-book"])
class ReferenceBookView(ListAPIView):
    permission_classes = [ReferenceBookPermission]

    model_serializer = {
        "milfaculties": (Milfaculty, MilfacultySerializer),
        "milgroups": (Milgroup, MilgroupSerializer),
        "program": (Program, ProgramSerializer),
        "ranks": (Rank, RankSerializer),
        "rooms": (Room, RoomSerializer),
        "absence_time": (AbsenceTime, AbsenceTimeSerializer),
        "achievement_type": (AchievementType, AchievementTypeSerializer),
    }

    def list(self, request, *args, **kwargs):
        # pylint:disable=(too-many-locals)
        if request.data:
            titles = request.data["filter_by"]
        else:
            titles = self.model_serializer.keys()
        response = {}
        for title in titles:
            model, serializer = self.model_serializer[title]
            response[title] = serializer(model.objects.all(), many=True).data

        return Response(response)


@extend_schema(tags=["reference-book"])
class MilfacultyViewSet(ModelViewSet):
    serializer_class = MilfacultySerializer
    queryset = Milfaculty.objects.all()

    permission_classes = [ReadOnly | ReferenceBookPermission]


@extend_schema(tags=["reference-book"])
class MilspecialtyViewSet(ModelViewSet):
    serializer_class = MilspecialtySerializer
    queryset = Milspecialty.objects.all()

    permission_classes = [ReadOnly | ReferenceBookPermission]

    filter_backends = [DjangoFilterBackend]
    filterset_class = MilspecialtyFilter


@extend_schema(tags=["reference-book"])
class MilgroupViewSet(ModelViewSet):
    serializer_class = MilgroupSerializer
    queryset = Milgroup.objects.order_by("title")

    permission_classes = [ReadOnly | ReferenceBookPermission]

    filter_backends = [DjangoFilterBackend]
    filterset_class = MilgroupFilter

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return MilgroupMutateSerializer
        return MilgroupSerializer


@extend_schema(tags=["reference-book"])
class ProgramViewSet(ModelViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.order_by("code")

    permission_classes = [ReadOnly | ReferenceBookPermission]

    filterset_class = ProgramFilter


@extend_schema(tags=["reference-book"])
class RankViewSet(ModelViewSet):
    serializer_class = RankSerializer
    queryset = Rank.objects.all()

    permission_classes = [ReadOnly | ReferenceBookPermission]


@extend_schema(tags=["reference-book"])
class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=["reference-book"])
class AbsenceTimeViewSet(ModelViewSet):
    serializer_class = AbsenceTimeSerializer
    queryset = AbsenceTime.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=["reference-book"])
class AchievementTypeViewSet(ModelViewSet):
    serializer_class = AchievementTypeSerializer
    queryset = AchievementType.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=["reference-book"])
class SkillViewSet(ModelViewSet):
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()

    permission_classes = [ReferenceBookPermission]


@extend_schema(tags=["reference-book"],
               parameters=[
                   OpenApiParameter(name="milfaculty",
                                    description="Filter by milfaculty ID",
                                    required=True,
                                    type=int),
               ],
               responses={200: MilgroupLeadersPhonesSerializer})
class MilgroupLeadersView(APIView):

    def get(self, request):
        students = Student.objects.select_related(
            "milgroup",
            "milgroup__milfaculty",
            "contact_info",
        ).filter(
            milgroup__milfaculty__id=request.query_params["milfaculty"],
            post=Student.Post.MILGROUP_COMMANDER.value,
        )
        phones = [
            s.contact_info.personal_phone_number
            for s in students
            if s.contact_info
        ]
        response = {"phones": phones}
        return Response(response)
