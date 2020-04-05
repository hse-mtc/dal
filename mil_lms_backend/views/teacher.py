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

from mil_lms_backend.serializers import TeacherSerializer
from mil_lms_backend.models import Teacher


@permission_classes((AllowAny,))
class TeacherView(APIView):
    def get(self, request: Request) -> Response:
        '''
        GET syntax examples:
        .../teacher/
        .../teacher/?id=3
        .../students/?&name=Ivan
        :param request:
        :return:
        '''

        teachers = Teacher.objects.all()

        # get by id
        if 'id' in request.query_params:
            teacher = teachers.get(id=request.query_params['id'])
            teacher = TeacherSerializer(teacher)
            return Response({'code': HTTP_200_OK * 100, 'teachers': teacher.data}, status=HTTP_200_OK)
        
        # get by name
        if 'name' in request.query_params:
           teachers =teachers.annotate(
                search_name=Lower(Concat('surname', Value(' '), 'name', Value(' '), 'patronymic')))
           teachers =teachers.filter(search_name__contains=request.query_params['name'].lower())
        
        teachers = TeacherSerializer(teachers, many=True)
        return Response({'code': HTTP_200_OK * 100, 'teachers': teachers.data}, status = HTTP_200_OK)
    
    
    def put(self, request: Request) -> Response:
        """
        Create new student
        PUT function - data is given via 'data' from PUT request (not query!)
        :param request:
        :return:
        """
        teacher = TeacherSerializer(data=request.data)
        if teacher.is_valid():
            teacher = teacher.save()
            return Response({'code': HTTP_200_OK * 100,
                             'message': f'Teacher with id {teacher.id} successfully created'},
                            status=HTTP_200_OK)
        else:
            return Response({'code': HTTP_400_BAD_REQUEST * 100,
                             'message': teacher.errors},
                            status=HTTP_400_BAD_REQUEST)


    def post(self, request: Request) -> Response:
        """
        POST function - data is given via 'data' from POST request (not query!)
        :param request:
        :return:
        """
        teacher = Teacher.objects.filter(id=request.data['id'])
        if teacher.exists():
            teacher_ser = TeacherSerializer(data=request.data)
            if teacher_ser.is_valid():
                teacher_ser.update(instance=teacher, validated_data=request.data)
                return Response({'code': HTTP_200_OK * 100,
                                 'message': f'Teacher with id {request.data["id"]} successfully modified'},
                                status=HTTP_200_OK)
            else:
                return Response({'code': HTTP_400_BAD_REQUEST * 100,
                                 'message': student_ser.errors},
                                status=HTTP_400_BAD_REQUEST)
        else:
            return Response({'code': HTTP_400_BAD_REQUEST * 100,
                             'message': f'Teacher with id {request.data["id"]} does not exist in this database'},
                            status=HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
        """
        DELETE - function uses id from request 'query'
        :param request:
        :return:
        """
        teacher_to_delete = Teacher.objects.filter(id=request.query_params['id'])
        if teacher_to_delete.exists():
            teacher_to_delete.delete()
            return Response({'code': HTTP_200_OK * 100,
                            'message': f'Teacher with id {request.query_params["id"]} successfully deleted'},
                            status=HTTP_200_OK)
        else:
            return Response({'code': HTTP_400_BAD_REQUEST * 100,
                            'message': f'Teacher with id {request.query_params["id"]} does not exist in this database'},
                            status=HTTP_400_BAD_REQUEST)
