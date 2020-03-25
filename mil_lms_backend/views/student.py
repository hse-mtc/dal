# coding=utf-8

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
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from mil_lms_backend.serializers import StudentSerializer
from mil_lms_backend.models import Student


@permission_classes((AllowAny,))
class StudentView(APIView):
    def get(self, request: Request) -> Response:
        """
        GET syntax examples:
        .../students/
        .../students/?id=3
        .../students/?milgroup=1234&name=Ivan
        :param request:
        :return:
        """
        students = Student.objects.all()

        # get by id
        if 'id' in request.query_params:
            student = students.get(id=request.query_params['id'])
            student = StudentSerializer(student)
            return Response({'code': HTTP_200_OK * 100, 'students': student.data}, status=HTTP_200_OK)

        # filter milgroup
        if 'milgroup' in request.query_params:
            students = students.filter(milgroup=request.query_params['milgroup'])

        # filter name
        if 'name' in request.query_params:
            students = students.annotate(
                search_name=Lower(Concat('surname', Value(' '), 'name', Value(' '), 'patronymic')))
            students = students.filter(search_name__contains=request.query_params['name'].lower())
        # filter status
        if 'status' in request.query_params:
            students = students.filter(status=request.query_params['status'])

        students = StudentSerializer(students, many=True)
        return Response({'code': HTTP_200_OK * 100, 'students': students.data}, status=HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """
        POST function - data is given via 'data' from POST request (not query!)
        :param request:
        :return:
        """
        student = StudentSerializer(data=request.data)
        if student.is_valid(raise_exception=True):
            student = student.save()
            return Response({'code': HTTP_201_CREATED * 100,
                             'message': f'Student with id {student.id} successfully created'},
                            status=HTTP_201_CREATED)

    def delete(self, request: Request) -> Response:
        """
        DELETE - function uses id from request 'query'
        :param request:
        :return:
        """
        student_to_delete = Student.objects.filter(id=request.query_params['id'])
        if student_to_delete.exists():
            student_to_delete.delete()
            return Response({'code': HTTP_200_OK * 100,
                             'message': f'Student with id {request.query_params["id"]} successfully deleted'},
                            status=HTTP_200_OK)
        else:
            return Response({'code': HTTP_400_BAD_REQUEST * 100,
                             'message': f'Student with id {request.query_params["id"]} does not exist in this database'},
                            status=HTTP_400_BAD_REQUEST)
