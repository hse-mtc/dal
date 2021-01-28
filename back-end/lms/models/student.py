from django.db import models

from common.models.persons import Person
from lms.models.common import Milgroup


class Status(models.Model):
    status = models.CharField(primary_key=True, max_length=20)

    def __str__(self):
        return str(self.status)

    class Meta:
        verbose_name = 'Student Status'
        verbose_name_plural = 'Student Statuses'


class Program(models.Model):
    code = models.CharField(primary_key=True, max_length=8)
    program = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'({str(self.code)}) {str(self.program)}'

    class Meta:
        verbose_name = 'Educational Program'
        verbose_name_plural = 'Educational Programs'


class Student(Person):
    milgroup = models.ForeignKey(Milgroup, models.DO_NOTHING)
    birthdate = models.DateField()
    program = models.ForeignKey(Program, models.DO_NOTHING)
    status = models.ForeignKey(Status, models.DO_NOTHING)
    photo = models.ImageField(upload_to = '', max_length=128)
    place_birth = models.TextField()
    region = models.TextField()
    adress = models.TextField()
    pasport = models.TextField() #можно числовой, но проще так
    pasport_ufms = models.TextField()
    pasport_ufms_code = models.TextField()
    pasport_date = models.DateField()
    citizence = models.TextField()
    fio_rod = models.TextField()
    hse_id = models.TextField()
    faculty = models.TextField()
    edu_program = models.TextField()
    hse_group = models.TextField()
    #mother
    mother_fio = models.TextField()
    mother_birthday = models.DateField()
    mother_place_of_birth = models.TextField()
    mother_citizence = models.TextField()
    
    #father
    father_fio = models.TextField()
    father_birthday = models.DateField()
    father_place_of_birth = models.TextField()
    father_citizence = models.TextField()
    
    #sister
    sister_fio = models.TextField()
    sister_birthday = models.DateField()
    sister_place_of_birth = models.TextField()
    sister_citizence = models.TextField()
    
    #brother
    brother_fio = models.TextField()
    brother_birthday = models.DateField()
    brother_place_of_birth = models.TextField()
    brother_citizence = models.TextField()
    
    pers_mobile = models.TextField()
    corp_email = models.TextField()
    pers_email = models.TextField()
    rel_mobile = models.TextField()
    
    voenkom_city = models.TextField()
    voenkom_district = models.TextField()
    
    vus = models.TextField()
    
    
    

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Full name = {str(self.surname)} ' \
               f'{str(self.name)} {str(self.patronymic)}\n'

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
