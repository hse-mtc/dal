import datetime

from django.db import models

from lms.models.students import Student
from lms.models.teachers import Teacher


class Encouragement(models.Model):

    class EncouragementType(models.TextChoices):
        ENCOURAGEMENT = 'EN', 'Благодарность'
        REMOVE_PUNISHMENT = 'RE', 'Снятие взыскания'

    student = models.ForeignKey(Student, models.DO_NOTHING)
    reason = models.CharField(max_length=200)
    encouragement_type = models.CharField(max_length=2, choices=EncouragementType.choices)
    date = models.DateField(default=datetime.date.today)
    teacher = models.ForeignKey(Teacher, models.DO_NOTHING)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'StudentID = {str(self.student)}, ' \
               f'TeacherID = {str(self.teacher)}\n' \
               f'Type = {str(self.encouragement_type)}\n' \
               f'Date = {str(self.date)}'

    class Meta:
        verbose_name = 'Encouragement Journal'
        verbose_name_plural = 'Encouragement Journal'
