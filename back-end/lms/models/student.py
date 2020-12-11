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
    photo = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Full name = {str(self.surname)} ' \
               f'{str(self.name)} {str(self.patronymic)}\n'

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
