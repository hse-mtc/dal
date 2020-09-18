# pylint: disable=duplicate-code
from datetime import timedelta, datetime

from django.db import IntegrityError
from django.db.models import Value
from django.db.models.functions import (
    Lower,
    Concat,
)

from django.views.decorators.csrf import csrf_exempt

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from lms.serializers import (
    MilgroupSerializer,
    AbsenceSerializer,
    AbsenceGetQuerySerializer,
)
from lms.models import Absence, Milgroup


def get_date_range(date_from, date_to, weekday):
    start_date = date_from + timedelta((weekday - date_from.weekday() + 7) % 7)

    dates = []
    cur_date = start_date
    
    while cur_date <= date_to:
        dates.append(cur_date.strftime('%d.%m.%Y'))
        cur_date += timedelta(7)

    return dates


@permission_classes((AllowAny,))
class AbsenceView(APIView):

    @csrf_exempt
    def get(self, request: Request) -> Response:
        """
        Get absent record or records
        GET syntax examples:
        .../absence/
        .../absence/?id=2
        .../absence/?studentid=3&date=...
        :param request:
        :return:
        """
        # check query params
        query_params = AbsenceGetQuerySerializer(data=request.query_params)
        if not query_params.is_valid():
            return Response({'message': query_params.errors},
                            status=HTTP_400_BAD_REQUEST)

        absences = Absence.objects.all()

        # get by id
        if 'id' in request.query_params:
            absence = absences.get(id=request.query_params['id'])
            absence = AbsenceSerializer(absence)
            return Response({'students': absence.data}, status=HTTP_200_OK)

        # filter by date
        if 'date_from' in request.query_params:
            absences = absences.filter(
                date__gte=request.query_params['date_from'])

        if 'date_to' in request.query_params:
            absences = absences.filter(
                date__lte=request.query_params['date_to'])

        # filter by studentid
        if 'studentid' in request.query_params:
            absences = absences.filter(
                studentid=request.query_params['studentid'])

        # filter by milgroup
        if 'milgroup' in request.query_params:
            absences = absences.filter(
                studentid__milgroup__milgroup=request.query_params['milgroup'])

        # filter by name
        if 'name' in request.query_params:
            absences = absences.annotate(search_name=Lower(
                Concat('studentid__surname', Value(' '), 'studentid__name',
                       Value(' '), 'studentid__patronymic')))
            absences = absences.filter(
                search_name__contains=request.query_params['name'].lower())

        # filter by type
        if 'absenceType' in request.query_params:
            absences = absences.filter(
                absenceType=request.query_params['absenceType'])

        # filter by status
        if 'absenceStatus' in request.query_params:
            absences = absences.filter(
                absenceStatus=request.query_params['absenceStatus'])

        absences = AbsenceSerializer(absences, many=True)
        return Response({'absences': absences.data}, status=HTTP_200_OK)

    # pylint: disable=no-self-use
    @csrf_exempt
    def put(self, request: Request) -> Response:
        """
        Create new absence record.
        PUT function - data is given via 'data' from PUT request (not query!)
        :param request:
        :return:
        """
        absence = AbsenceSerializer(data=request.data)
        try:
            if absence.is_valid():
                absence = absence.save()
                return Response(
                    {
                        'message': f'Absence record with id {absence.id} '
                                   f'successfuly created'
                    },
                    status=HTTP_200_OK)
            return Response({'message': absence.errors},
                            status=HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(
                {
                    'message': 'A record with this student and this date '
                               'already exists. Please, modify existing record.'
                },
                status=HTTP_400_BAD_REQUEST)
    
    # pylint: disable=no-self-use
    @csrf_exempt
    def post(self, request: Request) -> Response:
        """
        Modify absence record.
        POST function - data is given via 'data' from POST request (not query!)
        Payload example:
        {
            "id": 1,
            "date": "21.01.2020",
            "absenceType": "Уважительная",
            "studentid": {
                "name": "Артем",
                "surname": "Кацевалов"
            },
            "reason": "Заболел",
            "absenceStatus": "Закрыт",
            "comment": "Болеть будет недолго"
        }
        :param request:
        :return:
        """
        existing_absence = Absence.objects.filter(id=request.data['id'])
        if existing_absence.exists():
            absence_ser = AbsenceSerializer(data=request.data)
            if absence_ser.is_valid():
                absence_ser.update(instance=existing_absence,
                                   validated_data=request.data)
                return Response(
                    {
                        'message': f'Absence with id {request.data["id"]} '
                                   f'successfully modified'
                    },
                    status=HTTP_200_OK)
            return Response({'message': absence_ser.errors},
                            status=HTTP_400_BAD_REQUEST)
        return Response(
            {
                'message': f'Absence with id {request.data["id"]} '
                           f'does not exist in this database'
            },
            status=HTTP_400_BAD_REQUEST)
    
    # pylint: disable=no-self-use
    @csrf_exempt
    def delete(self, request: Request) -> Response:
        """
        DELETE - function uses id from request 'query'
        :param request:
        :return:
        """
        absence_to_delete = Absence.objects.filter(
            id=request.query_params['id'])
        if absence_to_delete.exists():
            absence_to_delete.delete()
            return Response(
                {
                    'message': f'Absence with id {request.query_params["id"]} '
                               f'successfully deleted'
                },
                status=HTTP_200_OK)
        return Response(
            {
                'message': f'Absence with id {request.query_params["id"]} '
                           f'does not exist in this database'
            },
            status=HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class AbsenceJournalView(APIView):

    @csrf_exempt
    def get(self, request: Request) -> Response:
        """
        Get absent records in the form of journal
        GET syntax example:
        .../absence_journal/?milgroup=1809&datefrom=...&dateto=...
        :param request:
        :return:
        """
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
