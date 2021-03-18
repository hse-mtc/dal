import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from common.models.subjects import Subject
from lms.models.common import Milgroup


class Room(models.Model):
    room = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return f'{str(self.room)}'

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'


class Lesson(models.Model):

    class Type(models.TextChoices):
        LECTURE = 'LE', 'Лекция'
        SEMINAR = 'SE', 'Семинар'
        GROUP = 'GR', 'Групповое занятие'
        PRACTICE = 'PR', 'Практическое занятие'
        FINAL_TEST = 'FI', 'Зачет'
        EXAM = 'EX', 'Экзамен'

    lesson_type = models.CharField(max_length=2, choices=Type.choices)
    subject = models.ForeignKey(Subject, models.DO_NOTHING)
    room = models.ForeignKey(Room, models.DO_NOTHING)
    milgroup = models.ForeignKey(Milgroup, models.DO_NOTHING)
    # TODO: How to add teacher? Teacher is not connected to subjects
    # But it would be good to have this connection (to set teachers by default).
    # This field should be here to handle situations
    # where teachers are substituted
    # teacher = models.ForeignKey(Teacher, models.DO_NOTHING)

    date = models.DateField(default=datetime.date.today)
    # Lesson #1, #2, #3, etc
    # Номер пары короче
    ordinal = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10),
                    MinValueValidator(1)])

    def __str__(self):
        return f'Lesson {str(self.subject)} on {str(self.date)}, ' \
               f'#{str(self.ordinal)}'

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
