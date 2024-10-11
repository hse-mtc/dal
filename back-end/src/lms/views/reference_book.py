from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema, OpenApiParameter

from common.constants import MUTATE_ACTIONS

from common.models.milspecialties import Milspecialty
from common.models.universities import Program

from common.serializers.milspecialties import (
    MilspecialtySerializer,
    WithSelectableByProgramMilspecialtySerializer,
)
from common.serializers.universities import ProgramSerializer

from common.filters.milspecialties import MilspecialtyFilter
from common.filters.universities import ProgramFilter

from auth.models import Permission
from auth.permissions import (
    BasePermission,
    ReadOnly,
)

from lms.models.absences import AbsenceTime
from lms.models.achievements import AchievementType
from lms.models.lessons import Room
from lms.models.teachers import Teacher
from lms.models.common import (
    Milfaculty,
    Milgroup,
)
from lms.models.students import (
    Student,
    Skill,
)

from lms.serializers.absences import AbsenceTimeSerializer
from lms.serializers.achievements import AchievementTypeSerializer
from lms.serializers.lessons import RoomSerializer
from lms.serializers.students import SkillSerializer
from lms.serializers.common import (
    MilfacultySerializer,
    MilgroupSerializer,
    MilgroupMutateSerializer,
    MilgroupLeadersPhonesSerializer,
)

from lms.filters.reference_books import MilgroupFilter

from lms.utils.mixins import QuerySetScopingMixin

from lms.types.personnel import Personnel


class ReferenceBookPermission(BasePermission):
    permission_class = "reference-books"
    view_name_rus = "Справочные данные"


class MilgroupPermission(BasePermission):
    permission_class = "milgroups"
    view_name_rus = "Взвода"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
    ]


@extend_schema(tags=["reference-book"])
class ReferenceBookView(ListAPIView):
    permission_classes = [ReferenceBookPermission]

    model_serializer = {
        "milfaculties": (Milfaculty, MilfacultySerializer),
        "milgroups": (Milgroup, MilgroupSerializer),
        "program": (Program, ProgramSerializer),
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
    def get_serializer_class(self):
        if "program" in self.request.query_params:
            return WithSelectableByProgramMilspecialtySerializer
        return MilspecialtySerializer

    queryset = Milspecialty.objects.all()

    permission_classes = [ReadOnly | ReferenceBookPermission]

    filter_backends = [DjangoFilterBackend]
    filterset_class = MilspecialtyFilter

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="program",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Show if selectable by program",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        program = request.query_params.get("program")
        if program is not None:
            try:
                # Attempt to convert the program to an integer
                int(program)
            except ValueError:
                # If conversion fails, raise a validation error
                raise ValidationError(
                    {"program": "Program must be a valid integer."},
                    code=status.HTTP_400_BAD_REQUEST,
                )
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["reference-book"])
class MilgroupViewSet(QuerySetScopingMixin, ModelViewSet):
    serializer_class = MilgroupSerializer
    queryset = Milgroup.objects.order_by("title")

    permission_allow_read_only = True
    permission_classes = [ReadOnly | MilgroupPermission]
    scoped_permission_class = MilgroupPermission

    filter_backends = [DjangoFilterBackend]
    filterset_class = MilgroupFilter

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return MilgroupMutateSerializer
        return MilgroupSerializer

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, kwargs["pk"])
        serializer = MilgroupSerializer(
            self.get_object(),
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def handle_scope_milfaculty(self, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        return self.queryset.filter(milfaculty=milfaculty)


@extend_schema(tags=["reference-book"])
class ProgramViewSet(ModelViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.order_by("code")

    permission_classes = [ReadOnly | ReferenceBookPermission]

    filter_backends = [DjangoFilterBackend]
    filterset_class = ProgramFilter


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


@extend_schema(
    tags=["reference-book"],
    parameters=[
        OpenApiParameter(
            name="milfaculty",
            description="Filter by milfaculty ID",
            required=True,
            type=int,
        ),
    ],
    responses={200: MilgroupLeadersPhonesSerializer},
)
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
            s.contact_info.personal_phone_number for s in students if s.contact_info
        ]
        response = {"phones": phones}
        return Response(response)
