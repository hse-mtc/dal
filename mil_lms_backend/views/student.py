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
    HTTP_400_BAD_REQUEST,
)

from mil_lms_backend.serializers import StudentSerializer, StudentQuerySerializer
from mil_lms_backend.models import Student


@permission_classes((AllowAny,))
class StudentView(APIView):
    def get(self, request: Request) -> Response:
        """
        Get student or students
        GET syntax examples:
        .../student/
        .../student/?id=3
        .../student/?milgroup=1234&name=Ivan
        :param request:
        :return:
        """
        students = Student.objects.all()
        # check query params
        query_params = StudentQuerySerializer(data=request.query_params)
        if not query_params.is_valid():
            return Response({'code': HTTP_400_BAD_REQUEST * 100, 
                             'message': query_params.errors},
                            status=HTTP_400_BAD_REQUEST)
        # get by id
        if 'id' in request.query_params:
            student = students.get(id=request.query_params['id'])
            student = StudentSerializer(student)
            return Response({'code': HTTP_200_OK * 100, 
                             'students': student.data}, 
                            status=HTTP_200_OK)

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

    def put(self, request: Request) -> Response:
        """
        Create new student
        PUT function - data is given via 'data' from PUT request (not query!)
        :param request:
        :return:
        """
        student = StudentSerializer(data=request.data)
        if student.is_valid():
            student = student.save()
            return Response({'code': HTTP_200_OK * 100,
                             'message': f'Student with id {student.id} successfully created'},
                            status=HTTP_200_OK)
        else:
            return Response({'code': HTTP_400_BAD_REQUEST * 100,
                             'message': student.errors},
                            status=HTTP_400_BAD_REQUEST)

    def post(self, request: Request) -> Response:
        """
        Modify existing student
        POST function - data is given via 'data' from POST request (not query!)
        :param request:
        :return:
        """
        existing_student = Student.objects.filter(id=request.data['id'])
        if existing_student.exists():
            student_ser = StudentSerializer(data=request.data)
            if student_ser.is_valid():
                student_ser.update(instance=existing_student, validated_data=request.data)
                return Response({'code': HTTP_200_OK * 100,
                                 'message': f'Student with id {request.data["id"]} successfully modified'},
                                status=HTTP_200_OK)
            else:
                return Response({'code': HTTP_400_BAD_REQUEST * 100,
                                 'message': student_ser.errors},
                                status=HTTP_400_BAD_REQUEST)
        else:
            return Response({'code': HTTP_400_BAD_REQUEST * 100,
                             'message': f'Student with id {request.data["id"]} does not exist in this database'},
                            status=HTTP_400_BAD_REQUEST)

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
