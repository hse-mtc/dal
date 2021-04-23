from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from drf_spectacular.views import extend_schema, OpenApiParameter

from lms.models.teachers import Teacher
from lms.serializers.teachers import TeacherSerializer
from lms.models.students import Student
from lms.serializers.students import StudentSerializer
from lms.serializers.persons import PersonsQuerySerializer
from lms.functions import search_persons, persons_response

from auth.permissions import BasePermission


class UserPermission(BasePermission):
    permission_class = 'auth.user'


@extend_schema(tags=['persons'],
               parameters=[
                   OpenApiParameter(name='name',
                                    description='Filter by fullname',
                                    required=True,
                                    type=str),
               ])
class PersonView(APIView):

    permission_classes = [UserPermission]

    def get(self, request):
        query_params = PersonsQuerySerializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)

        name = request.query_params['name']

        students = search_persons(Student, StudentSerializer, name)
        teachers = search_persons(Teacher, TeacherSerializer, name)

        data = persons_response(students) + persons_response(teachers)

        return Response(data, status=HTTP_200_OK)
