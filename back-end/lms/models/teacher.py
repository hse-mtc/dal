from django.db import models

from common.models import Person
from lms.models.common import Milfaculty, Milgroup


class Rank(models.Model):
    rank = models.CharField(primary_key=True, max_length=30)

    def __str__(self):
        return str(self.rank)

    class Meta:
        db_table = 'rank'
        verbose_name = 'Military Rank'
        verbose_name_plural = 'Military Ranks'


class TeacherPost(models.Model):
    teacher_post = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.teacher_post)

    class Meta:
        db_table = 'teacher_post'
        verbose_name = 'Teacher Post'
        verbose_name_plural = 'Teacher Posts'


class Teacher(Person):
    milfaculty = models.ForeignKey(Milfaculty,
                                   models.DO_NOTHING,
                                   db_column='milfaculty')
    rank = models.ForeignKey(Rank, models.DO_NOTHING, db_column='rank')
    teacher_post = models.ForeignKey(TeacherPost,
                                     models.DO_NOTHING,
                                     db_column='teacher_post')
    milgroup = models.ForeignKey(Milgroup,
                                 models.DO_NOTHING,
                                 db_column='milgroup',
                                 blank=True,
                                 null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Full name = {str(self.surname)} ' \
               f'{str(self.name)} {str(self.patronymic)}\n'

    class Meta:
        db_table = 'teacher'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
