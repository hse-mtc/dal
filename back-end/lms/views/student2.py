from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from lms.views.viewsets import GetPutPostDeleteModelViewSet, filter_names
from lms.models import Student
from lms.serializers import (
    StudentSerializer, StudentGetQuerySerializer
)


class StudentViewSet(GetPutPostDeleteModelViewSet):
    serializer_class = StudentSerializer
    query_params_serializer_class = StudentGetQuerySerializer
    queryset = Student.objects.all()
    
    permission_classes = [AllowAny]

    get_filters = ['milgroup', 'status']
    special_get_filters = {'name': filter_names}

