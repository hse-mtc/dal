import datetime

from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)

from common.models.subjects import Subject

from lms.models.common import Milgroup
from lms.models.teachers import Teacher


class Room(models.Model):
    title = models.CharField(
        unique=True,
        max_length=63,
    )

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    class Type(models.TextChoices):
        LECTURE = "LE", "Лекция"
        SEMINAR = "SE", "Семинар"
        GROUP = "GR", "Групповое занятие"
        PRACTICE = "PR", "Практическое занятие"
        FINAL_TEST = "FI", "Зачет"
        EXAM = "EX", "Экзамен"

    type = models.CharField(
        max_length=2,
        choices=Type.choices,
    )
    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        to=Room,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    # TODO(gakhromov, TmLev): ideally, this should be M2M, because there can
    #   be lectures for the entire milfaculty (many milgroups simultaneously).
    milgroup = models.ForeignKey(
        to=Milgroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    teacher = models.ForeignKey(
        to=Teacher,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    date = models.DateField(default=datetime.date.today)

    # Lesson #1, #2, #3, etc
    # Номер пары короче
    ordinal = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return f"Lesson {self.subject} on {self.date}, #{self.ordinal}"
