from datetime import datetime

from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.views import (
    OpenApiParameter,
    extend_schema,
)

from common.constants import MUTATE_ACTIONS

from common.views.choices import GenericChoicesList

from common.utils.date import get_date_range

from auth.models import Permission
from auth.permissions import BasePermission

from lms.models.common import Milgroup
from lms.models.lessons import Lesson
from lms.models.students import Student
from lms.models.teachers import Teacher

from lms.serializers.common import MilgroupSerializer
from lms.serializers.lessons import (
    LessonSerializer,
    LessonJournalQuerySerializer,
    LessonMutateSerializer,
)

from lms.filters.lessons import LessonFilter

from lms.utils.mixins import QuerySetScopingMixin
from lms.utils.functions import milgroup_allowed_by_scope

from lms.types.personnel import Personnel


class LessonPermission(BasePermission):
    permission_class = "lessons"
    view_name_rus = "Расписание занятий"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
        Permission.Scope.MILGROUP,
    ]


@extend_schema(tags=["lessons"])
class LessonViewSet(QuerySetScopingMixin, ModelViewSet):
    queryset = Lesson.objects.all()

    permission_classes = [LessonPermission]
    scoped_permission_class = LessonPermission

    filter_backends = [DjangoFilterBackend]

    filterset_class = LessonFilter

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return LessonMutateSerializer
        return LessonSerializer

    def handle_scope_milfaculty(self, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        return self.queryset.filter(milgroup__milfaculty=milfaculty)

    def allow_scope_milfaculty_on_create(self, data, personnel: Personnel):
        # this milgroup must exist as permission check occurs after
        # the serializer validation
        milgroup = Milgroup.objects.get(id=data["milgroup"])

        match personnel:
            case Student() | Teacher():
                return milgroup.milfaculty == personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

    def handle_scope_milgroup(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.filter(milgroup=personnel.milgroup)
            case Teacher():
                return self.queryset.filter(milgroup__in=personnel.milgroups)
            case _:
                assert False, "Unhandled Personnel type"

    def allow_scope_milgroup_on_create(self, data, personnel: Personnel):
        match personnel:
            case Student():
                return data["milgroup"] == personnel.milgroup.id
            case Teacher():
                milgroup_ids = personnel.milgroups.values_list("id", flat=True)
                return data["milgroup"] in milgroup_ids
            case _:
                assert False, "Unhandled Personnel type"


@extend_schema(tags=["lesson-journal"],
               parameters=[
                   OpenApiParameter(name="milgroup",
                                    description="Filter by milgroup",
                                    required=True,
                                    type=int),
                   OpenApiParameter(name="date_from",
                                    description="Filter by date",
                                    required=True,
                                    type=OpenApiTypes.DATE),
                   OpenApiParameter(name="date_to",
                                    description="Filter by date",
                                    required=True,
                                    type=OpenApiTypes.DATE),
               ])
class LessonJournalView(GenericAPIView):
    permission_classes = [LessonPermission]

    # pylint: disable=too-many-locals
    def get(self, request: Request) -> Response:
        query_params = LessonJournalQuerySerializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)

        # final json
        data = {}

        # add milgroup data
        milgroup = Milgroup.objects.get(id=request.query_params["milgroup"])

        # this check restricts all journal access if scope == SELF
        # TODO(@gakhromov): mb allow scope == SELF for journal requests
        if not milgroup_allowed_by_scope(milgroup, request, LessonPermission):
            return Response(
                {
                    "detail":
                        "You do not have permission to perform this action."
                },
                status=status.HTTP_403_FORBIDDEN)

        milgroup = MilgroupSerializer(milgroup).data
        data["milgroup"] = milgroup

        # calculate dates
        date_from = datetime.fromisoformat((query_params.data["date_from"]))
        date_to = datetime.fromisoformat((query_params.data["date_to"]))

        date_range = get_date_range(date_from, date_to, milgroup["weekday"])
        data["dates"] = date_range

        # sort lessons by date and milgroup
        lessons_filtered = Lesson.objects.filter(
            milgroup=request.query_params["milgroup"],
            date__gte=request.query_params["date_from"],
            date__lte=request.query_params["date_to"])

        # ordinals
        ordinals = []
        for ordinal in range(1, 11):
            lessons = {
                "ordinal": ordinal,
                "lessons": LessonSerializer(
                    lessons_filtered.filter(ordinal=ordinal),
                    many=True
                ).data
            }
            ordinals.append(lessons)

        data["ordinals"] = ordinals

        return Response(data, status=status.HTTP_200_OK)


@extend_schema(tags=["lessons", "choices"])
class LessonTypeChoicesList(GenericChoicesList):
    choices_class = Lesson.Type
