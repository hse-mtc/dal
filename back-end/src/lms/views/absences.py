from datetime import datetime

from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

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

from lms.functions import get_date_range

from lms.views.archived_viewset import ArchivedModelViewSet

from auth.permissions import BasePermission


class AbsencePermission(BasePermission):
    permission_class = 'auth.absence'


@extend_schema(tags=['absences'])
class AbsenceViewSet(ArchivedModelViewSet):
    queryset = Absence.objects.all()

    permission_classes = [AbsencePermission]
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
        if not query_params.is_valid():
            return Response(query_params.errors, status=HTTP_400_BAD_REQUEST)

        # final json
        data = {}

        # add milgroup data
        milgroup = MilgroupSerializer(
            Milgroup.objects.get(
                milgroup=request.query_params['milgroup'])).data
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

        return Response(data, status=HTTP_200_OK)
