from rest_framework.permissions import AllowAny

from lms.views.viewsets import GetPutPostDeleteModelViewSet
from lms.models import Student
from lms.serializers.student import (StudentSerializer,
                                     StudentGetQuerySerializer)
from lms.filters import StudentFilterSet


class StudentViewSet(GetPutPostDeleteModelViewSet):
    serializer_class = StudentSerializer
    query_params_serializer_class = StudentGetQuerySerializer
    queryset = Student.objects.all()

    permission_classes = [AllowAny]

    filterset_class = StudentFilterSet
    search_fields = ['surname', 'name', 'patronymic']
