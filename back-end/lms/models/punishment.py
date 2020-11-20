import datetime

from django.db import models

from lms.models.student import Student
from lms.models.teacher import Teacher


class PunishmentType(models.Model):
    punishment_type = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.punishment_type)

    class Meta:
        db_table = 'punishment_type'
        verbose_name = 'Punishment Type'
        verbose_name_plural = 'Punishment Types'


class Punishment(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING, db_column='student')
    reason = models.CharField(max_length=200)
    punishment_type = models.ForeignKey(PunishmentType,
                                        models.DO_NOTHING,
                                        db_column='punishment_type')
    date = models.DateField(default=datetime.date.today)
    teacher = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='teacher')
    remove_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'StudentID = {str(self.student)}, ' \
               f'TeacherID = {str(self.teacher)}\n' \
               f'Type = {str(self.punishment_type)}\n' \
               f'Date = {str(self.date)}, ' \
               f'Remove Date = {str(self.remove_date)}'

    class Meta:
        db_table = 'punishment'
        verbose_name = 'Punishment Journal'
        verbose_name_plural = 'Punishment Journal'
