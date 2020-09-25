from rest_framework.permissions import AllowAny

from lms.views.viewsets import GetPutPostDeleteModelViewSet
from lms.models import Teacher
from lms.serializers.teacher import (TeacherSerializer,
                                     TeacherGetQuerySerializer)
from lms.filters import TeacherFilterSet


class TeacherViewSet(GetPutPostDeleteModelViewSet):
    serializer_class = TeacherSerializer
    query_params_serializer_class = TeacherGetQuerySerializer
    queryset = Teacher.objects.all()

    permission_classes = [AllowAny]

    filterset_class = TeacherFilterSet
    search_fields = ['surname', 'name', 'patronymic']
