from datetime import timedelta, datetime

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from lms.serializers.common import MilgroupSerializer
from lms.serializers.absence import (AbsenceSerializer,
                                     AbsenceJournalSerializer,
                                     AbsenceJournalGetQuerySerializer)

from lms.models.common import Milgroup
from lms.models.absence import Absence
from lms.models.student import Student

from lms.filters.absence import AbsenceFilter


def get_date_range(date_from, date_to, weekday):
    start_date = date_from + timedelta((weekday - date_from.weekday() + 7) % 7)

    dates = []
    cur_date = start_date

    while cur_date <= date_to:
        dates.append(cur_date.strftime('%Y-%m-%d'))
        cur_date += timedelta(7)

    return dates


@extend_schema(tags=['absence'])
class AbsenceViewSet(ModelViewSet):
    serializer_class = AbsenceSerializer
    queryset = Absence.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = AbsenceFilter
    search_fields = ['student__surname', 'student__name', 'student__patronymic']


@extend_schema(tags=['absence-journal'])
class AbsenceJournalView(GenericAPIView):
    permission_classes = [AllowAny]

    # pylint: disable=too-many-locals
    def get(self, request: Request) -> Response:
        query_params = AbsenceJournalGetQuerySerializer(
            data=request.query_params)
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
