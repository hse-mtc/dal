# coding=utf-8

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

from mil_lms_backend.models import Absence


@permission_classes((AllowAny,))
class AbsenceView(APIView):
    def get(self, request: Request) -> Response:
        """
        """
        absences = Absence.objects.all()
        
        return Response({'code': HTTP_200_OK * 100,
                         'absences': []},
                        status=HTTP_200_OK)