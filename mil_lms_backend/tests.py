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
        # test get all
        response = client.get('/api/lms/student/')
        from_api = response.data['students']
        
        from_db = StudentSerializer(Student.objects.all(), many=True).data
        
        self.assertEqual(from_api, from_db)
        self.assertEqual(response.status_code*100, response.data['code'])
        
        # test for id
        response = client.get('/api/lms/student/', {'id': 2})
        from_api = response.data['students']
        
        from_db = StudentSerializer(Student.objects.get(id=2)).data
        
        self.assertEqual(from_api, from_db)
        self.assertEqual(response.status_code*100, response.data['code'])
        
        # test for non-existing id
        response = client.get('/api/lms/student/', {'id': 100})
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
        # test for bad type id
        response = client.get('/api/lms/student/', {'id': 'crazy_input'})
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
        # test for id + some other search query
        response = client.get('/api/lms/student/', {'id': 2, 'milgroup':2020})
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
        # test for milgroup
        response = client.get('/api/lms/student/', {'milgroup': 2020})
        from_api = response.data['students']
        
        from_db = StudentSerializer(Student.objects.filter(milgroup=2020), many=True).data
        
        self.assertEqual(from_api, from_db)
        self.assertEqual(response.status_code*100, response.data['code'])
        
        # test for non-existing milgroup
        response = client.get('/api/lms/student/', {'milgroup': 100})
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
        # test for bad type milgroup
        response = client.get('/api/lms/student/', {'milgroup': 'crazy_input'})
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
        # test for exisiting names
        response = client.get('/api/lms/student/', {'name': 'Иван'})
        from_api = response.data['students']
        
        from_db = StudentSerializer(Student.objects.filter(id=1), many=True).data
        
        self.assertEqual(from_api, from_db)
        self.assertEqual(response.status_code*100, response.data['code'])
        
        # test for non-exisiting names
        response = client.get('/api/lms/student/', {'name': 'crazy_input'})
        from_api = response.data['students']
        
        from_db = []
        
        self.assertEqual(from_api, from_db)
        self.assertEqual(response.status_code*100, response.data['code'])
        
        # test for exisiting status
        response = client.get('/api/lms/student/', {'status': 'Обучается'})
        from_api = response.data['students']
        
        from_db = StudentSerializer(Student.objects.all(), many=True).data
        
        self.assertEqual(from_api, from_db)
        self.assertEqual(response.status_code*100, response.data['code'])
        
        # test for non-exisiting status
        response = client.get('/api/lms/student/', {'status': 'crazy_input'})
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
