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
from lms.serializers.absences import (AbsenceSerializer,
                                      AbsenceJournalSerializer,
                                      AbsenceJournalQuerySerializer,
                                      AbsenceMutateSerializer)

from lms.models.common import Milgroup
from lms.models.absences import Absence
from lms.models.students import Student

from lms.filters.absences import AbsenceFilter
from lms.functions import get_date_range, milgroup_allowed_by_scope
from lms.mixins import StudentTeacherQuerySetScopingMixin, ArchivedMixin

from lms.functions import get_date_range

from auth.models import Permission
from auth.permissions import BasePermission


class AbsencePermission(BasePermission):
    permission_class = 'absences'
    view_name_rus = 'Пропуски'
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
        Permission.Scope.MILGROUP,
        Permission.Scope.SELF,
    ]


@extend_schema(tags=['absences'])
class AbsenceViewSet(ArchivedMixin, StudentTeacherQuerySetScopingMixin, ModelViewSet):
    queryset = Absence.objects.all()

    permission_classes = [AbsencePermission]
    scoped_permission_class = AbsencePermission

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = AbsenceFilter
    search_fields = ['student__surname', 'student__name', 'student__patronymic']

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return AbsenceMutateSerializer
        return AbsenceSerializer


@extend_schema(tags=['absence-journal'],
               parameters=[
                   OpenApiParameter(name='milgroup',
                                    description='Filter by milgroup',
                                    required=True,
                                    type=int),
                   OpenApiParameter(name='date_from',
                                    description='Filter by date',
                                    required=True,
                                    type=OpenApiTypes.DATE),
                   OpenApiParameter(name='date_to',
                                    description='Filter by date',
                                    required=True,
                                    type=OpenApiTypes.DATE),
               ])
class AbsenceJournalView(GenericAPIView):
    permission_classes = [AbsencePermission]

    # pylint: disable=too-many-locals
    def get(self, request: Request) -> Response:
        query_params = AbsenceJournalQuerySerializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)

        # final json
        data = {}

        # add milgroup data
        milgroup = MilgroupSerializer(
            Milgroup.objects.get(
                milgroup=request.query_params['milgroup'])).data

        # this check restricts all journal access if scope == SELF
        # TODO(@gakhromov): mb allow scope == SELF for journal requests
        if not milgroup_allowed_by_scope(milgroup, request, AbsencePermission):
            return Response(
                {
                    'detail':
                        'You do not have permission to perform this action.'
                },
                status=status.HTTP_403_FORBIDDEN)

        data['milgroup'] = milgroup

        # calculate dates
        date_from = datetime.fromisoformat(query_params.data['date_from'])
        date_to = datetime.fromisoformat(query_params.data['date_to'])

        date_range = get_date_range(date_from, date_to, milgroup['weekday'])

        # add dates and absences
        data['dates'] = date_range
        data['students'] = AbsenceJournalSerializer(
            Student.objects.filter(
                milgroup__milgroup=request.query_params['milgroup']),
            context={
                'request': request,
                'date_range': date_range,
            },
            many=True).data

        return Response(data, status=status.HTTP_200_OK)
