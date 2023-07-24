from datetime import datetime

from rest_framework import status

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)

from common.constants import MUTATE_ACTIONS

from common.models.subjects import Subject

from auth.models import Permission
from auth.permissions import BasePermission

from lms.models.common import Milgroup
from lms.models.marks import Mark
from lms.models.students import Student
from lms.models.teachers import Teacher
from lms.models.lessons import Lesson

from lms.serializers.common import MilgroupSerializer
from lms.serializers.subjects import LessonSubjectSerializer
from lms.serializers.lessons import LessonSerializer
from lms.serializers.marks import (
    MarkSerializer,
    MarkMutateSerializer,
    MarkHistorySerializer,
    MarkJournalSerializer,
    MarkJournalQuerySerializer,
)

from lms.filters.marks import (
    MarkFilter,
    MarkHistoryFilter,
)

from lms.utils.functions import milgroup_allowed_by_scope
from lms.utils.mixins import QuerySetScopingMixin

from lms.types.personnel import Personnel


class MarkPermission(BasePermission):
    permission_class = "marks"
    view_name_rus = "Оценки"
    methods = ["get", "put", "post", "patch", "delete"]
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
        Permission.Scope.MILGROUP,
        Permission.Scope.SELF,
    ]

    methods_str = {
        "get": ": получение данных",
        "post": ": создание данных",
        "put": ": добавление пересдач",
        "patch": ": редактирование последней оценки",
        "delete": ": удаление последней оценки",
    }


@extend_schema(tags=["marks"])
class MarkViewSet(QuerySetScopingMixin, ModelViewSet):
    # pylint: disable=too-many-public-methods
    queryset = Mark.objects.all()

    permission_classes = [MarkPermission]
    scoped_permission_class = MarkPermission

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = MarkFilter
    search_fields = ["student__surname", "student__name", "student__patronymic"]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return MarkMutateSerializer
        return MarkSerializer

    # override POST - new mark
    # pylint: disable=W1113
    # pylint: disable=W0221
    def create(self, request, *args, **kwargs):
        request.data["values"] = [request.data.pop("value")]
        request.data["changed_by"] = request.user.pk
        return super().create(request, *args, **kwargs)

    # override PUT - add mark to array
    # pylint: disable=W1113,W0221
    def update(self, request, pk=None, *args, **kwargs):
        qs = self.get_queryset()
        if not qs.exists():
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        request.data["values"] = qs.get(id=pk).values + [request.data["value"]]
        request.data["changed_by"] = request.user.pk
        return super().update(request, pk, partial=True, *args, **kwargs)

    # override PATCH - change last mark in array
    # pylint: disable=W1113,W0221
    def partial_update(self, request, pk=None, *args, **kwargs):
        qs = self.get_queryset()
        if not qs.exists():
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        request.data["values"] = qs.get(id=pk).values
        request.data["values"][-1] = request.data["value"]
        request.data["changed_by"] = request.user.pk
        return super().update(request, pk, partial=True, *args, **kwargs)

    # override DELETE - delete last mark in array
    # pylint: disable=W1113,W0221
    def destroy(self, request, pk=None, *args, **kwargs):
        qs = self.get_queryset()
        if not qs.exists():
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        request.data["values"] = qs.get(id=pk).values
        request.data["values"].pop(-1)
        request.data["changed_by"] = request.user.pk
        if len(request.data["values"]) == 0:
            return super().destroy(request, pk, *args, **kwargs)
        return super().update(request, pk, *args, **kwargs)

    def handle_scope_milfaculty(self, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        return self.queryset.filter(student__milgroup__milfaculty=milfaculty)

    def allow_scope_milfaculty_on_create(self, data, personnel: Personnel):
        # no need to check student existence,
        # as permission check occurs after
        # serializer validation
        student = Student.objects.get(id=data["student"])

        match personnel:
            case Student() | Teacher():
                return student.milgroup.milfaculty == personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

    def handle_scope_milgroup(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.filter(student__milgroup=personnel.milgroup)
            case Teacher():
                return self.queryset.filter(student__milgroup__in=personnel.milgroups)
            case _:
                assert False, "Unhandled Personnel type"

    def allow_scope_milgroup_on_create(self, data, personnel: Personnel):
        # no need to check student existence,
        # as permission check occurs after
        # serializer validation
        student = Student.objects.get(id=data["student"])

        match personnel:
            case Student():
                return student.milgroup == personnel.milgroup
            case Teacher():
                return student.milgroup in personnel.milgroups
            case _:
                assert False, "Unhandled Personnel type"

    def handle_scope_self(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.filter(student=personnel)
            case Teacher():
                return self.queryset.none()
            case _:
                assert False, "Unhandled Personnel type"

    def allow_scope_self_on_create(self, data, personnel: Personnel):
        match personnel:
            case Student():
                return data["student"] == personnel.id
            case Teacher():
                return False
            case _:
                assert False, "Unhandled Personnel type"


@extend_schema(tags=["marks-history"])
class MarkHistoryViewSet(QuerySetScopingMixin, ModelViewSet):
    # pylint: disable=too-many-public-methods
    permission_classes = [MarkPermission]
    scoped_permission_class = MarkPermission

    filterset_class = MarkHistoryFilter
    queryset = Mark.history.all()
    serializer_class = MarkHistorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]

    search_fields = ["student__surname", "student__name", "student__patronymic"]

    def handle_scope_milfaculty(self, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        return self.queryset.filter(student__milgroup__milfaculty=milfaculty)

    def handle_scope_milgroup(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.filter(student__milgroup=personnel.milgroup)
            case Teacher():
                return self.queryset.filter(student__milgroup__in=personnel.milgroups)
            case _:
                assert False, "Unhandled Personnel type"

    def handle_scope_self(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.filter(student=personnel)
            case Teacher():
                return self.queryset.none()
            case _:
                assert False, "Unhandled Personnel type"


@extend_schema(
    tags=["mark-journal"],
    parameters=[
        OpenApiParameter(
            name="milgroup", description="Filter by milgroup", required=True, type=int
        ),
        OpenApiParameter(
            name="subject", description="Filter by subject", required=True, type=int
        ),
        OpenApiParameter(
            name="date_from",
            description="Filter by date",
            required=True,
            type=OpenApiTypes.DATE,
        ),
        OpenApiParameter(
            name="date_to",
            description="Filter by date",
            required=True,
            type=OpenApiTypes.DATE,
        ),
    ],
)
class MarkJournalView(GenericAPIView):
    permission_classes = [MarkPermission]
    scoped_permission_class = MarkPermission

    # pylint: disable=too-many-locals
    def get(self, request: Request) -> Response:
        query_params = MarkJournalQuerySerializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)

        # final json
        data = {}

        # add milgroup data
        milgroup = Milgroup.objects.get(id=request.query_params["milgroup"])

        if not milgroup_allowed_by_scope(
            milgroup, request, self.scoped_permission_class
        ):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        milgroup = MilgroupSerializer(milgroup).data
        data["milgroup"] = milgroup

        subject_query = Subject.objects.get(id=request.query_params["subject"])
        subject = LessonSubjectSerializer(subject_query).data
        data["subject"] = subject

        # calculate dates
        date_from = datetime.fromisoformat(query_params.data["date_from"])
        date_to = datetime.fromisoformat(query_params.data["date_to"])

        milgroup_id = request.query_params["milgroup"]

        # date_range = get_date_range(date_from, date_to, milgroup["weekday"])
        lessons = Lesson.objects.filter(
            date__lte=date_to,
            date__gte=date_from,
            milgroup=milgroup_id,
            subject=request.query_params["subject"],
        ).order_by("date", "ordinal")
        data["lessons"] = LessonSerializer(lessons, many=True).data
        date_range = list({item.date for item in lessons})

        # add dates and absences
        data["dates"] = sorted(date_range)

        # get students
        # if scope == SELF, return only one student
        scope = request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, request.method
        )

        if scope == Permission.Scope.SELF:
            filter_kwargs = {"user": request.user}
        else:
            filter_kwargs = {"milgroup": milgroup_id}
        data["students"] = MarkJournalSerializer(
            Student.objects.filter(**filter_kwargs),
            context={
                "request": request,
                "date_range": date_range,
                "subject": subject_query.id,
            },
            many=True,
        ).data

        return Response(data, status=status.HTTP_200_OK)
