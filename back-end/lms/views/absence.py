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
        required_params = ['milgroup', 'date_from', 'date_to']
        for req_param in required_params:
            if req_param not in request.query_params:
                return Response(
                    {'message': f'Please, insert {req_param} as a query parameter.'},
                    status=HTTP_400_BAD_REQUEST)
        

        absences = Absence.objects.filter(
            studentid__milgroup__milgroup=request.query_params['milgroup'])
        
        data = {}

        # add milgroup data
        milgroup = MilgroupSerializer(Milgroup.objects.get(
            milgroup=request.query_params['milgroup'])).data
        data['milgroup'] = milgroup

        # calculate dates
        date_from = datetime.strptime(request.query_params['date_from'], '%d.%m.%Y')
        date_to = datetime.strptime(request.query_params['date_to'], '%d.%m.%Y')

        if date_to < date_from:
            return Response({'message': 'date_from should be greater or equal to date_to.'}, 
                            status=HTTP_400_BAD_REQUEST)
        
        date_ranges = get_date_range(date_from, date_to, milgroup['weekday'])
        

        # get absences
        students = {}
        for date in date_ranges:
            date_f = datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d')
            # absences for today
            absence = Absence.objects.filter(date=date_f)
            if absence.count() > 0:
                absences = AbsenceSerializer(absence, many=True).data
                # parse each absence
                for absence in absences:
                    studentid = absence['studentid']['id']
                    if studentid not in students:
                        students[studentid] = {
                            'id': studentid,
                            'fullname': absence['studentid']['fullname'],
                            'absences': []
                        }
                    students[studentid]['absences'] = {
                        date: {
                            'absenceType': absence['absenceType'],
                            'absenceStatus': absence['absenceStatus'],
                            'reason': absence['reason'],
                            'comment': absence['comment']
                        }
                    }


        data['dates'] = date_ranges
        data['students'] = list(students.values())

        return Response({'absences': data}, status=HTTP_200_OK)
