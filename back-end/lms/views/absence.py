from django.db.models.query import QuerySet
from django.db.models import Value
from django.db.models.functions import (
    Lower,
    Concat,
)

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from lms.serializers.absence import (
    AbsenceSerializer,
    AbsenceGetQuerySerializer,
)
from lms.models import Absence
from lms.views.viewsets import GetPutPostDeleteModelViewSet


def filter_names_studentid(items: QuerySet, request: Request) -> QuerySet:
    items = items.annotate(search_name=Lower(
        Concat('studentid__surname', Value(' '), 'studentid__name', Value(' '),
               'studentid__patronymic')))
    items = items.filter(
        search_name__contains=request.query_params['name'].lower())
    return items


class AbsenceViewSet(GetPutPostDeleteModelViewSet):
    serializer_class = AbsenceSerializer
    query_params_serializer_class = AbsenceGetQuerySerializer
    queryset = Absence.objects.all()

    permission_classes = [AllowAny]

    get_filters = ['student_id', 'absenceType', 'absenceStatus']
    special_get_filters = {
        'name': filter_names_studentid,
        'milgroup': lambda items, request:
                        items.filter(studentid__milgroup__milgroup=
                                request.query_params['milgroup']),
        'date_from': lambda items, request: 
                        items.filter(date__gte=request.query_params['date_from']),
        'date_to': lambda items, request: 
                        items.filter(date__lte=request.query_params['date_to']),
    }


class AbsenceJournalView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """
        Get absent records in the form of journal
        GET syntax example:
        .../absence_journal/?milgroup=1809
        :param request:
        :return:
        """
        if 'milgroup' not in request.query_params:
            return Response(
                {'message': 'Please, insert milgroup as a query parameter.'},
                status=HTTP_400_BAD_REQUEST)

        absences = Absence.objects.filter(
            studentid__milgroup__milgroup=request.query_params['milgroup'])
        return Response({'absences': absences.data}, status=HTTP_200_OK)
