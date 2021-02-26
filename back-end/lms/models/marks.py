from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from django.db import models

from lms.models.lessons import Lesson
from lms.models.students import Student


class Mark(models.Model):
    mark = ArrayField(
        models.IntegerField(
            validators=[MaxValueValidator(5),
                        MinValueValidator(2)]))
    lesson = models.ForeignKey(Lesson, models.DO_NOTHING)
    student = models.ForeignKey(Student, models.DO_NOTHING)

    def __str__(self):
        return f'Mark {str(self.mark)} for student id=' \
               f'{str(self.student)} on lesson id={str(self.lesson)}'

    class Meta:
        verbose_name = 'Mark'
        verbose_name_plural = 'Marks'
