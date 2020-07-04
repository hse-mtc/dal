from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from django.test import TestCase, Client
from django.urls import reverse

# import models and serializers
from mil_lms_backend.models import (
    Student, Milgroup, Milfaculty, Program, Status
)
from mil_lms_backend.serializers import (
    StudentSerializer,
)


client = Client()


class StudentViewTest(TestCase):
    def setUp(self):
        # create test faculty, group, program and status
        milf = Milfaculty.objects.create(milfaculty='ВКС')
        milgr1 = Milgroup.objects.create(milgroup=2020, milfaculty=milf)
        milgr2 = Milgroup.objects.create(milgroup=2021, milfaculty=milf)
        prog = Program.objects.create(code='01.01.01',
                                      program='Видосы индусов с ютуба')
        stat = Status.objects.create(status='Обучается')
        # create test students
        Student.objects.create(surname='Петров',
                               name='Иван',
                               patronymic='Сергеевич',
                               milgroup=milgr1,
                               birthdate='2000-11-04',
                               program=prog,
                               status=stat)
        Student.objects.create(surname='Сидоров',
                               name='Павел',
                               patronymic='Александрович',
                               milgroup=milgr2,
                               birthdate='1999-08-23',
                               program=prog,
                               status=stat)
    
    def test_get(self):
        tests = [
            {'uri': '/api/lms/student/', 'query': {},  # test get all 
             'response_wrapper_for_equality_check': lambda response: getattr(response, 'data')['students'],
             'true_value_for_equality_check': StudentSerializer(Student.objects.all(), many=True).data},
            
            {'uri': '/api/lms/student/', 'query': {'id': 2},  # test for id 
             'response_wrapper_for_equality_check': lambda response: getattr(response, 'data')['students'],
             'true_value_for_equality_check': StudentSerializer(Student.objects.get(id=2)).data},
            
            {'uri': '/api/lms/student/', 'query': {'id': 100},  # test for non-existing id
             'response_wrapper_for_equality_check': lambda response: getattr(response, 'status_code'),
             'true_value_for_equality_check': HTTP_400_BAD_REQUEST},
            
            {'uri': '/api/lms/student/', 'query': {'id': 'crazy_input'},  # test for bad type id
             'response_wrapper_for_equality_check': lambda response: getattr(response, 'status_code'),
             'true_value_for_equality_check': HTTP_400_BAD_REQUEST},
            
            {'uri': '/api/lms/student/', 'query': {'id': 'crazy_input', 'milgroup': 2020},  # test for id + some other search query
             'response_wrapper_for_equality_check': lambda response: getattr(response, 'status_code'),
             'true_value_for_equality_check': HTTP_400_BAD_REQUEST},
            
            {'uri': '/api/lms/student/', 'query': {'milgroup': 2020},  # test for milgroup
             'response_wrapper_for_equality_check': lambda response: getattr(response, 'data')['students'],
             'true_value_for_equality_check': StudentSerializer(Student.objects.filter(milgroup=2020), many=True).data},
            
            {'uri': '/api/lms/student/', 'query': {'milgroup': 100},  # test for non-existing milgroup
             'response_wrapper_for_equality_check': lambda response: getattr(response, 'status_code'),
             'true_value_for_equality_check': HTTP_400_BAD_REQUEST},
            
            {'uri': '/api/lms/student/', 'query': {'milgroup': 'crazy_input'},  # test for bad type milgroup
             'response_wrapper_for_equality_check': lambda response: getattr(response, 'status_code'),
             'true_value_for_equality_check': HTTP_400_BAD_REQUEST},
            
            {'uri': '/api/lms/student/', 'query': {'name': 'Иван'},  # test for exisiting names
             'response_wrapper_for_equality_check': lambda response: getattr(response, 'data')['students'],
             'true_value_for_equality_check': StudentSerializer(Student.objects.filter(id=1), many=True).data},
            
            {'uri': '/api/lms/student/', 'query': {'name': 'crazy_input'},  # test for non-exisiting names
             'response_wrapper_for_equality_check': lambda response: getattr(response, 'data')['students'],
             'true_value_for_equality_check': []},
            
            {'uri': '/api/lms/student/', 'query': {'status': 'Обучается'},  # test for exisiting status
             'response_wrapper_for_equality_check': lambda response: getattr(response, 'data')['students'],
             'true_value_for_equality_check': StudentSerializer(Student.objects.all(), many=True).data},
            
            {'uri': '/api/lms/student/', 'query': {'status': 'crazy_input'}, # test for non-exisiting status
             'response_wrapper_for_equality_check': lambda response: getattr(response, 'status_code'),
             'true_value_for_equality_check': HTTP_400_BAD_REQUEST},
        ]
        
        for i, test in enumerate(tests):
            response = client.get(test['uri'], test['query'])
            from_api = test['response_wrapper_for_equality_check'](response)
            from_db = test['true_value_for_equality_check']
            
            try:
                self.assertEqual(from_api, from_db)
                self.assertEqual(response.status_code * 100, response.data['code'])
            except AssertionError as err:
                print('$' * 70)
                print(f'~~~ Failed on GET test #{i} ~~~')
                raise err
