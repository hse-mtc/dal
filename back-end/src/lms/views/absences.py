from datetime import datetime

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rest_framework.generics import GenericAPIView

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from common.constants import MUTATE_ACTIONS

from lms.serializers.common import MilgroupSerializer
from lms.serializers.absences import (
    AbsenceSerializer,
    AbsenceJournalSerializer,
    AbsenceJournalQuerySerializer,
    AbsenceMutateSerializer,
)

from lms.models.common import Milgroup
from lms.models.absences import Absence
from lms.models.students import Student

from lms.filters.absences import AbsenceFilter
from lms.utils.functions import get_date_range, milgroup_allowed_by_scope
from lms.utils.mixins import QuerySetScopingMixin

from auth.models import Permission
from auth.permissions import BasePermission


class AbsencePermission(BasePermission):
    permission_class = "absences"
    view_name_rus = "Пропуски"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
        Permission.Scope.MILGROUP,
        Permission.Scope.SELF,
    ]


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

    def handle_scope_milfaculty(self, user_type, user):
        if user_type == "student":
            return self.queryset.filter(
                student__milgroup__milfaculty=user.milgroup.milfaculty)
        if user_type == "teacher":
            return self.queryset.filter(
                student__milgroup__milfaculty=user.milfaculty)
        return self.queryset.none()

    def allow_scope_milfaculty_on_create(self, data, user_type, user):
        student = Student.objects.filter(id=data["student"])
        if not student.exists():
            return False
        student = student.first()

        if user_type == "student":
            return user.milgroup.milfaculty == student.milgroup.milfaculty
        if user_type == "teacher":
            return user.milfaculty == student.milgroup.milfaculty

        return False

    def handle_scope_milgroup(self, user_type, user):
        if user_type == "student":
            return self.queryset.filter(student__milgroup=user.milgroup)

        if user_type == "teacher":
            return self.queryset.filter(student__milgroup__in=user.milgroups)

        return self.queryset.none()

    def allow_scope_milgroup_on_create(self, data, user_type, user):
        student = Student.objects.filter(id=data["student"])
        if not student.exists():
            return False
        student = student.first()

        if user_type == "student":
            return student.milgroup == user.milgroup

        if user_type == "teacher":
            return student.milgroup in user.milgroups

        return False

    def handle_scope_self(self, user_type, user):
        if user_type == "student":
            return self.queryset.filter(student=user)
        return self.queryset.none()

    def allow_scope_self_on_create(self, data, user_type, user):
        if user_type == "student":
            return data["student"] == user.id
        return False


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
class AbsenceJournalView(GenericAPIView):
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
