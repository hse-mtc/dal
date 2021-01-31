from django.db import models

from common.models.persons import Person, Personel, Relative
from lms.models.common import Milgroup

class Faculty(models.Model):
    faculty = models.CharField(primary_key=True, max_length=128, blank=True)

    def __str__(self):
        return str(self.faculty)

    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'


class Mil_specialty(models.Model):
    specialty_list = [('094001', 'Применение наземных подразделений войсковой разведки'),
                ('411300', 'Эксплуатация и ремонт автоматизированных систем комплексов баллистических стратегических ракет наземного базирования'),
                ('453000', 'Организация эксплуатации и ремонта автоматизированных систем управления и вычислительных комплексов ракетно-космической обороны'),
               ('453100', 'Математическое и программное обеспечение функционирования вычислительных комплексов ракетно-космической обороны'),
               ('751100','Защита информационных технологий'),
               ('100182', 'Стрелковые, командир стрелкового отделения'),
               ('106646-543', 'Разведывательные, разведчик-оператор СБР, ПСНР')]
    mil_specialty = models.CharField(primary_key=True, max_length=20, choices=specialty_list)

    def __str__(self):
        return str(self.mil_specialty)

    class Meta:
        verbose_name = 'Military specialty'
        verbose_name_plural = 'Military specialties'


class Status(models.Model):
    status_list = [('student', 'обучающийся'),
                   ('graduated', 'выпускник'),
                   ('deducted', 'отчислен'),
                   ('enrollee','абитуриент')]
    status = models.CharField(primary_key=True, max_length=20, choices=status_list)

    def __str__(self):
        return str(self.status)

    class Meta:
        verbose_name = 'Student Status'
        verbose_name_plural = 'Student Statuses'


class Program(models.Model):
    code = models.CharField(primary_key=True, max_length=8)
    program = models.CharField(max_length=128, blank=True, null=True)
    faculty = models.ForeignKey(Faculty, models.DO_NOTHING, blank=True)

    def __str__(self):
        return f'({str(self.code)}) {str(self.program)}'

    class Meta:
        verbose_name = 'Educational Program'
        verbose_name_plural = 'Educational Programs'
        

class Student(Personel):
    #militrary
    milgroup = models.ForeignKey(Milgroup, models.DO_NOTHING)
    commissariat_city = models.CharField(max_length=32)
    commissariat_district = models.CharField(max_length=32)
    mil_specialty = models.ForeignKey(Mil_specialty, models.DO_NOTHING)
    
    #student characteristics
    program = models.ForeignKey(Program, models.DO_NOTHING)
    status = models.ForeignKey(Status, models.DO_NOTHING)
    hse_id = models.CharField(max_length=32)
    hse_group = models.CharField(max_length=32)
    
    #passport information
    passport_series = models.CharField(max_length=4)
    passport_code = models.CharField(max_length=6)
    pasport_ufms_name = models.CharField(max_length=64)
    pasport_ufms_code = models.CharField(max_length=7)
    pasport_date = models.DateField()
    
    #family
    mother = models.ForeignKey(Relative, models.DO_NOTHING, related_name='mother')
    father = models.ForeignKey(Relative, models.DO_NOTHING, related_name='father')
    brother = models.ForeignKey(Relative, models.DO_NOTHING, related_name='brother')
    sister = models.ForeignKey(Relative, models.DO_NOTHING, related_name='sister')
    
    #name in genitive
    surname_genitive = models.CharField(max_length=32)
    name_genitive = models.CharField(max_length=32)
    patronymic_genetive = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Full name = {str(self.surname)} ' \
               f'{str(self.name)} {str(self.patronymic)}\n'

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
