from datetime import timedelta, datetime

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework.generics import GenericAPIView

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from lms.serializers.serializers import MilgroupSerializer
from lms.serializers.student import StudentShortSerializer
from lms.serializers.absence import (AbsenceSerializer,
                                     AbsenceGetQuerySerializer,
                                     AbsenceJournalSerializer,
                                     AbsenceJournalGetQuerySerializer)
from lms.models import Absence, Milgroup, Student
from lms.views.viewsets import GetPutPostDeleteModelViewSet
from lms.filters import AbsenceFilterSet


def get_date_range(date_from, date_to, weekday):
    start_date = date_from + timedelta((weekday - date_from.weekday() + 7) % 7)

    dates_iso = []
    dates = []
    cur_date = start_date

    while cur_date <= date_to:
        dates_iso.append(cur_date.strftime('%Y-%m-%d'))
        dates.append(cur_date.strftime('%d.%m.%Y'))
        cur_date += timedelta(7)

    return dates_iso, dates


class AbsenceViewSet(GetPutPostDeleteModelViewSet):
    serializer_class = AbsenceSerializer
    query_params_serializer_class = AbsenceGetQuerySerializer
    queryset = Absence.objects.all()

    permission_classes = [AllowAny]

    filterset_class = AbsenceFilterSet
    search_fields = [
        'studentid__surname', 'studentid__name', 'studentid__patronymic'
    ]


class AbsenceJournalView(GenericAPIView):
    serializer_class = AbsenceJournalSerializer

    permission_classes = [AllowAny]

    # pylint: disable=too-many-locals
    def get(self, request: Request) -> Response:
        query_params = AbsenceJournalGetQuerySerializer(
            data=request.query_params)
        if not query_params.is_valid():
            return Response(query_params.errors, status=HTTP_400_BAD_REQUEST)

        absences = Absence.objects.filter(
            studentid__milgroup__milgroup=request.query_params['milgroup'])

        # final json
        data = {}

        # add milgroup data
        milgroup = MilgroupSerializer(
            Milgroup.objects.get(
                milgroup=request.query_params['milgroup'])).data
        data['milgroup'] = milgroup

        # calculate dates
        date_from = datetime.strptime(request.query_params['date_from'],
                                      '%d.%m.%Y')
        date_to = datetime.strptime(request.query_params['date_to'], '%d.%m.%Y')

        if date_to < date_from:
            return Response(
                {'message': 'date_from should be greater or equal to date_to.'},
                status=HTTP_400_BAD_REQUEST)

        date_range_iso, date_range = \
                            get_date_range(date_from, date_to, milgroup['weekday'])
        # add dates and absneces
        data['dates'] = date_range
        data['students'] = AbsenceJournalSerializer(Student.objects.filter(milgroup__milgroup=request.query_params['milgroup']),
        context={
            "request": request,
            "date_range": date_range_iso,
        }, many=True).data

        return Response(data, status=HTTP_200_OK)
