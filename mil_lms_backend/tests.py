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

    def test_get_all(self):
        response = client.get('/api/lms/student/')
        from_api = response.data['students']
        
        from_db = StudentSerializer(Student.objects.all(), many=True).data
        
        self.assertEqual(from_api, from_db)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_get_id(self):
        # Even though there are only two entries in the db (id 1 and 2)
        # and django resets the db for each test, auto-increment function for id
        # still works and therefore ids get shifted for each test.
        # For this test, valid ids are 3 and 4.
        response = client.get('/api/lms/student/', {'id': 3})
        from_api = response.data['students']
        
        from_db = StudentSerializer(Student.objects.get(id=3)).data
        
        self.assertEqual(from_api, from_db)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_get_id_non_existing(self):
        response = client.get('/api/lms/student/', {'id': 100})
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_get_id_bad_type(self):
        response = client.get('/api/lms/student/', {'id': 'crazy_input'})
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_get_id_plus_other_query(self):
        # See comment in test_get_for_id() for explanation on using 9 as a valid id.
        response = client.get('/api/lms/student/', {'id': 9, 'milgroup':2020})
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_get_milgroup(self):
        response = client.get('/api/lms/student/', {'milgroup': 2020})
        from_api = response.data['students']
        
        from_db = StudentSerializer(Student.objects.filter(milgroup=2020), many=True).data
        
        self.assertEqual(from_api, from_db)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_get_milgroup_non_existing(self):
        response = client.get('/api/lms/student/', {'milgroup': 100})
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_get_milgroup_bad_type(self):
        response = client.get('/api/lms/student/', {'milgroup': 'crazy_input'})
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_get_name(self):
        response = client.get('/api/lms/student/', {'name': 'Иван'})
        from_api = response.data['students']
        
        from_db = StudentSerializer(Student.objects.filter(name='Иван'), many=True).data
        
        self.assertEqual(from_api, from_db)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_get_name_non_exisiting(self):
        response = client.get('/api/lms/student/', {'name': 'crazy_input'})
        from_api = response.data['students']
        
        from_db = []
        
        self.assertEqual(from_api, from_db)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_get_status(self):
        response = client.get('/api/lms/student/', {'status': 'Обучается'})
        from_api = response.data['students']
        
        from_db = StudentSerializer(Student.objects.all(), many=True).data
        
        self.assertEqual(from_api, from_db)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_get_status_non_exisiting(self):
        response = client.get('/api/lms/student/', {'status': 'crazy_input'})
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_put(self):
        new_student = {
            'milgroup': {
                'milgroup': 2020,
                'milfaculty': 'ВКС'
            },
            'program': {
                'code': '01.01.01',
                'program': 'Видосы индусов с ютуба'
            },
            'birthdate': '01.01.1999',
            'surname': 'Новенький',
            'name': 'Рекрут',
            'patronymic': 'Студент',
            'photo': None,
            'status': 'Обучается'
        }
        response = client.put('/api/lms/student/', new_student, content_type='application/json')
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_200_OK)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_put_missing_field(self):
        new_student = {
            'milgroup': {  
                'milgroup': 2020,
                'milfaculty': 'ВКС'
            },  # error here, no program given
            'birthdate': '01.01.1999',
            'surname': 'Новенький',
            'name': 'Рекрут',
            'patronymic': 'Студент',
            'photo': None,
            'status': 'Обучается'
        }
        response = client.put('/api/lms/student/', new_student, content_type='application/json')
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_put_empty(self):
        new_student = {}
        response = client.put('/api/lms/student/', new_student, content_type='application/json')
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_put_invalid_milgroup(self):
        new_student = {
            'milgroup': {  # error here
                'milgroup': 10000000000000,
                'milfaculty': 'не ВКС'
            },
            'program': {
                'code': '01.01.01',
                'program': 'Видосы индусов с ютуба'
            },
            'birthdate': '01.01.1999',
            'surname': 'Новенький',
            'name': 'Рекрут',
            'patronymic': 'Студент',
            'photo': None,
            'status': 'Обучается' 
        }
        response = client.put('/api/lms/student/', new_student, content_type='application/json')
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])

    def test_put_invalid_program(self):
        new_student = {
            'milgroup': { 
                'milgroup': 2020,
                'milfaculty': 'ВКС'
            },
            'program': {  # error here
                'code': '09.09.09',
                'program': 'Видосы индусов с ютуба'
            },
            'birthdate': '01.01.1999',
            'surname': 'Новенький',
            'name': 'Рекрут',
            'patronymic': 'Студент',
            'photo': None,
            'status': 'Обучается' 
        }
        response = client.put('/api/lms/student/', new_student, content_type='application/json')
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_put_invalid_birthdate(self):
        new_student = {
            'milgroup': { 
                'milgroup': 2020,
                'milfaculty': 'ВКС'
            },
            'program': { 
                'code': '01.01.01',
                'program': 'Видосы индусов с ютуба'
            },
            'birthdate': 'crazy_input', # error here
            'surname': 'Новенький',
            'name': 'Рекрут',
            'patronymic': 'Студент',
            'photo': None,
            'status': 'Обучается' 
        }
        response = client.put('/api/lms/student/', new_student, content_type='application/json')
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
    def test_put_invalid_status(self):
        new_student = {
            'milgroup': { 
                'milgroup': 2020,
                'milfaculty': 'ВКС'
            },
            'program': {  
                'code': '01.01.01',
                'program': 'Видосы индусов с ютуба'
            },
            'birthdate': '01.01.1999',
            'surname': 'Новенький',
            'name': 'Рекрут',
            'patronymic': 'Студент',
            'photo': None,
            'status': 'crazy_input'  # error here 
        }
        response = client.put('/api/lms/student/', new_student, content_type='application/json')
        from_api = response.status_code
        
        self.assertEqual(from_api, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.status_code*100, response.data['code'])
        
