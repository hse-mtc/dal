from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Value
from django.db.models.functions import Concat, Lower

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from mil_lms_backend import models
from mil_lms_backend import serializers


def index(response):
    return HttpResponse('Hello, world!')


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
        students_obj = models.Student.objects

        # get by id
        if 'id' in request.query_params:
            student = students_obj.get(id=request.query_params['id'])
            student = serializers.StudentSerializer(student)
            return Response(student.data, status=HTTP_200_OK)

        # filter milgroup
        if 'milgroup' not in request.query_params:
            students = students_obj.all()
        else:
            students = students_obj.filter(milgroup=request.query_params['milgroup'])

        # filter name
        if 'name' in request.query_params:
            students = students.annotate(
                search_name=Lower(Concat('surname', Value(' '), 'name', Value(' '), 'patronymic')))
            students = students.filter(search_name__contains=request.query_params['name'].lower())
        # filter status
        if 'status' in request.query_params:
            students = students.filter(status=request.query_params['status'])

        students = serializers.StudentSerializer(students, many=True)
        return Response({'students': students.data}, status=HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """
        POST function - data is given via 'data' from POST request (not query!)
        :param request:
        :return:
        """
        student = serializers.StudentSerializer(data=request.data)
        if student.is_valid(raise_exception=True):
            student = student.save()
            return Response({'message': 'Student with id %s successfully created' % student.id},
                            status=HTTP_201_CREATED)

    def delete(self, request: Request) -> Response:
        """
        DELETE - function uses id from request 'query'
        :param request:
        :return:
        """
        student_to_delete = models.Student.objects.filter(id=request.query_params['id'])
        if student_to_delete.exists():
            student_to_delete.delete()
            return Response({'message': 'Student with id %s successfully deleted' % request.query_params['id']},
                            status=HTTP_200_OK)
        else:
            return Response({'message': 'Student with id %s does not exist in this database' %
                                        request.query_params['id']}, status=HTTP_400_BAD_REQUEST)

    # TODO: finish writing patch method
    # def patch(self, request: Request) -> Response:
    #     """
    #     PATCH - used to modify existing student. Id is passed using request 'query'.
    #     Data to modify is passed via request 'data'
    #     :param request:
    #     :return:
    #     """
    #     student_to_modify = models.Student.objects.filter(id=request.query_params['id'])
    #     if student_to_modify.exists():
    #
    #         student_to_modify = student_to_modify[0]
    #         modified_columns = []
    #
    #         for key in request.data.keys():
    #             if key != 'id':
    #                 setattr(student_to_modify, key, request.data[key])
    #                 modified_columns.append(key)
    #
    #         student_to_modify.save(update_fields=modified_columns)
    #         student_to_modify = serializers.StudentSerializer(student_to_modify)
    #         return Response({'message': 'Student with id %s successfully modified' %
    #                                     request.query_params['id'],
    #                          'student': student_to_modify.data}, status=HTTP_200_OK)
    #     else:
    #         return Response({'message': 'Student with id %s does not exist in this database' %
    #                                     request.query_params['id']}, status=HTTP_400_BAD_REQUEST)
