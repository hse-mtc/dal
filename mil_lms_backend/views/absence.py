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

from mil_lms_backend.serializers import (
    AbsenceSerializer,
    AbsenceGetQuerySerializer,
)
from mil_lms_backend.models import Absence


@permission_classes((AllowAny,))
class AbsenceView(APIView):
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
            return Response({'code': HTTP_400_BAD_REQUEST * 100,
                             'message': query_params.errors},
                            status=HTTP_400_BAD_REQUEST)
        
        absences = Absence.objects.all()
        
        # get by id
        if 'id' in request.query_params:
            absence = absences.get(id=request.query_params['id'])
            absence = AbsenceSerializer(absence)
            return Response({'code': HTTP_200_OK * 100, 
                             'students': absence.data}, 
                            status=HTTP_200_OK)
        
        # filter by studentid
        if 'studentid' in request.query_params:
            absences = absences.filter(studentid=request.query_params['studentid'])
        
        # filter by name
        if 'name' in request.query_params:
            absences = absences.annotate(
                search_name=Lower(Concat('studentid__surname', Value(' '), 'studentid__name', Value(' '), 'studentid__patronymic'))
            )
            absences = absences.filter(search_name__contains=request.query_params['name'].lower())
        
        # filter by date
        if 'date' in request.query_params:
            absences = absences.filter(date=request.query_params['date'])
        
        # filter by type
        if 'absenceType' in request.query_params:
            absences = absences.filter(absenceType=request.query_params['absenceType'])
        
        absences = AbsenceSerializer(absences, many=True)
        return Response({'code': HTTP_200_OK * 100,
                         'absences': absences.data},
                        status=HTTP_200_OK)

    def put(self, request: Request) -> Response:
        """
        Create new absence record.
        PUT function - data is given via 'data' from PUT request (not query!)
        
        Payload example:
        {
            "date": "21.01.2020",
            "absenceType": "Уважительная",
            "studentid": {
                "name": "Артем",
                "surname": "Кацевалов"
            },
            "reason": "Заболел",
            "status": "1",
            "comment": "Болеть будет недолго"
        }
        :param request:
        :return:
        """
        absence = AbsenceSerializer(data=request.data)
        try:
            if absence.is_valid():
                absence = absence.save()
                return Response({'code': HTTP_200_OK * 100,
                                'message': f'Absence record with id {absence.id} successfuly created'},
                                status=HTTP_200_OK)
            else:
                return Response({'code': HTTP_400_BAD_REQUEST * 100,
                                'message': absence.errors},
                                status=HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'code': HTTP_400_BAD_REQUEST * 100,
                                'message': 'A record with this student and this date already exists. Please, modify existing record.'},
                                status=HTTP_400_BAD_REQUEST)
