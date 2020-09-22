from rest_framework.permissions import AllowAny

from lms.views.viewsets import GetPutPostDeleteModelViewSet, filter_names
from lms.models import Teacher
from lms.serializers.teacher import (
    TeacherSerializer, TeacherGetQuerySerializer)


class TeacherViewSet(GetPutPostDeleteModelViewSet):
    serializer_class = TeacherSerializer
    query_params_serializer_class = TeacherGetQuerySerializer
    queryset = Teacher.objects.all()

    permission_classes = [AllowAny]

    get_filters = ['milgroup', 'milfaculty', 'rank', 'teacherPost']
    special_get_filters = {'name': filter_names}
