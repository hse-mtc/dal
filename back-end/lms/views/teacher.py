# coding=utf-8

from django.db.models import Value
from django.db.models.functions import (
    Lower,
    Concat,
)

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

from lms.serializers import TeacherSerializer
from lms.models import Teacher


@permission_classes((AllowAny,))
class TeacherView(APIView):

    def get(self, request: Request) -> Response:
        '''
        GET syntax examples:
        .../teacher/
        .../teacher/?id=3
        .../teachers/?&name=Ivan
        :param request:
        :return:
        '''

        teachers = Teacher.objects.all()

        if 'id' in request.query_params:
            teacher = teachers.get(id=request.query_params['id'])
            teacher = TeacherSerializer(teacher)
            return Response({'teachers': teacher.data}, status=HTTP_200_OK)

        if 'name' in request.query_params:
            teachers = teachers.annotate(search_name=Lower(
                Concat('surname', Value(' '), 'name', Value(' '),
                       'patronymic')))
            teachers = teachers.filter(
                search_name__contains=request.query_params['name'].lower())

        if 'milfaculty' in request.query_params:
            teachers = teachers.filter(
                milfaculty=request.query_params['milfaculty'])

        teachers = TeacherSerializer(teachers, many=True)
        return Response({'teachers': teachers.data}, status=HTTP_200_OK)

    # pylint: disable=(no-self-use)
    def put(self, request: Request) -> Response:
        """
        Create new teacher
        PUT function - data is given via 'data' from PUT request (not query!)
        :param request:
        :return:
        """
        teacher = TeacherSerializer(data=request.data)
        if teacher.is_valid():
            teacher = teacher.save()
            return Response(
                {
                    'message':
                        f'Teacher with id {teacher.id} successfully created'
                },
                status=HTTP_200_OK)

        return Response({'message': teacher.errors},
                        status=HTTP_400_BAD_REQUEST)

    def post(self, request: Request) -> Response:
        """
        POST function - data is given via 'data' from POST request (not query!)
        :param request:
        :return:
        """
        teacher = Teacher.objects.filter(id=request.data['id'])

        if not teacher.exists():
            return Response(
                {
                    'message':
                        f'Teacher with id {request.data["id"]} '
                        f'does not exist in this database'
                },
                status=HTTP_400_BAD_REQUEST)

        teacher_ser = TeacherSerializer(data=request.data)

        if not teacher_ser.is_valid():
            return Response({'message': teacher_ser.errors},
                            status=HTTP_400_BAD_REQUEST)

        teacher_ser.update(instance=teacher, validated_data=request.data)
        return Response(
            {
                'message':
                    f'Teacher with id {request.data["id"]} '
                    f'successfully modified'
            },
            status=HTTP_200_OK)

    # pylint: disable=(no-self-use)
    def delete(self, request: Request) -> Response:
        """
        DELETE - function uses id from request 'query'
        :param request:
        :return:
        """
        teacher_to_delete = Teacher.objects.filter(
            id=request.query_params['id'])
        if teacher_to_delete.exists():
            teacher_to_delete.delete()
            return Response(
                {
                    'message':
                        f'Teacher with id {request.query_params["id"]} '
                        f'successfully deleted'
                },
                status=HTTP_201_CREATED)

        return Response(
            {
                'message':
                    f'Teacher with id {request.query_params["id"]} '
                    f'does not exist in this database'
            },
            status=HTTP_400_BAD_REQUEST)
