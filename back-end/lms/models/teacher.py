from django.db import models

from common.models import Person
from lms.models.common import Milfaculty, Milgroup


class Rank(models.Model):
    rank = models.CharField(primary_key=True, max_length=30)

    def __str__(self):
        return str(self.rank)

    class Meta:
        verbose_name = 'Military Rank'
        verbose_name_plural = 'Military Ranks'


class TeacherPost(models.Model):
    teacher_post = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.teacher_post)

    class Meta:
        verbose_name = 'Teacher Post'
        verbose_name_plural = 'Teacher Posts'


class Teacher(Person):
    milfaculty = models.ForeignKey(Milfaculty,
                                   models.DO_NOTHING)
    rank = models.ForeignKey(Rank, models.DO_NOTHING)
    teacher_post = models.ForeignKey(TeacherPost,
                                     models.DO_NOTHING)
    milgroup = models.ForeignKey(Milgroup,
                                 models.DO_NOTHING,
                                 blank=True,
                                 null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Full name = {str(self.surname)} ' \
               f'{str(self.name)} {str(self.patronymic)}\n'

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
