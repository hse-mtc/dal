from datetime import datetime

from rest_framework import status
from rest_framework import generics
from rest_framework import mixins

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

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
from lms.models.students import Student
from lms.models.teachers import Teacher
from lms.models.absences import (
    Absence,
    AbsenceTime,
    AbsenceAttachment,
)

from lms.serializers.common import MilgroupSerializer
from lms.serializers.absences import (
    AbsenceAttachmentSerializer,
    AbsenceJournalQuerySerializer,
    AbsenceJournalSerializer,
    AbsenceMutateSerializer,
    AbsenceSerializer,
    AbsenceTimeSerializer,
)

from lms.filters.absences import AbsenceFilter

from lms.utils.mixins import QuerySetScopingMixin
from lms.utils.functions import milgroup_allowed_by_scope

from lms.types.personnel import Personnel


class AbsencePermission(BasePermission):
    permission_class = "absences"
    view_name_rus = "Пропуски"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
        Permission.Scope.MILGROUP,
        Permission.Scope.SELF,
    ]


class AbsenceAttachmentPermission(BasePermission):
    permission_class = "absence-attachment"
    view_name_rus = "Приложения"
    methods = ["get", "delete"]
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
        Permission.Scope.MILGROUP,
        Permission.Scope.SELF,
    ]


@extend_schema(tags=["absence-attachment"])
class AbsenceAttachmentViewSet(mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               GenericViewSet):
    queryset = AbsenceAttachment.objects.all()
    serializer_class = AbsenceAttachmentSerializer
    permission_classes = [AbsenceAttachmentPermission]

    def destroy(self, request, pk=None, *args, **kwargs):
        return super().destroy(request, pk, *args, **kwargs)


@extend_schema(tags=["absences"])
class AbsenceViewSet(QuerySetScopingMixin, ModelViewSet):
    queryset = Absence.objects.all()

    permission_classes = [AbsencePermission]
    scoped_permission_class = AbsencePermission

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = AbsenceFilter
    search_fields = ["student__surname", "student__name", "student__patronymic"]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return AbsenceMutateSerializer
        return AbsenceSerializer

    def handle_scope_milfaculty(self, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        return self.queryset.filter(student__milgroup__milfaculty=milfaculty)

    def allow_scope_milfaculty_on_create(self, data, personnel: Personnel):
        student = Student.objects.filter(id=data["student"])
        if not student.exists():
            return False
        student = student.first()

        match personnel:
            case Student() | Teacher():
                return personnel.milfaculty == student.milgroup.milfaculty
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
        student = Student.objects.filter(id=data["student"])
        if not student.exists():
            return False
        student = student.first()

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


@extend_schema(tags=["absence-journal"],
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
class AbsenceJournalView(generics.GenericAPIView):
    permission_classes = [AbsencePermission]
    scoped_permission_class = AbsencePermission

    # pylint: disable=too-many-locals
    def get(self, request: Request) -> Response:
        query_params = AbsenceJournalQuerySerializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)

        # final json
        data = {}

        # add milgroup data
        milgroup = Milgroup.objects.get(id=request.query_params["milgroup"])

        if not milgroup_allowed_by_scope(milgroup, request,
                                         self.scoped_permission_class):
            return Response(
                {
                    "detail":
                        "You do not have permission to perform this action."
                },
                status=status.HTTP_403_FORBIDDEN)

        milgroup = MilgroupSerializer(milgroup).data
        data["milgroup"] = milgroup

        # calculate dates
        date_from = datetime.fromisoformat(query_params.data["date_from"])
        date_to = datetime.fromisoformat(query_params.data["date_to"])

        date_range = get_date_range(date_from, date_to, milgroup["weekday"])

        # add dates and absences
        data["dates"] = date_range

        # get students
        # if scope == SELF, return only one student
        scope = request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, request.method)

        if scope == Permission.Scope.SELF:
            filter_kwargs = {"user": request.user}
        else:
            filter_kwargs = {"milgroup__id": milgroup["id"]}

        data["students"] = AbsenceJournalSerializer(
            Student.objects.filter(**filter_kwargs),
            context={
                "request": request,
                "date_range": date_range,
            },
            many=True).data

        return Response(data, status=status.HTTP_200_OK)


@extend_schema(tags=["absence-time"])
class AbsenceTimeView(generics.RetrieveUpdateAPIView):
    serializer_class = AbsenceTimeSerializer
    queryset = AbsenceTime.objects.all()

    permission_classes = [AllowAny]

    def get_object(self) -> AbsenceTime:
        obj = AbsenceTime.objects.last()
        self.check_object_permissions(self.request, obj)
        return obj


@extend_schema(tags=["absences", "choices"])
class AbsenceExcuseChoicesList(GenericChoicesList):
    choices_class = Absence.Excuse


@extend_schema(tags=["absences", "choices"])
class AbsenceStatusChoicesList(GenericChoicesList):
    choices_class = Absence.Status
