import datetime

from django.db import models

from lms.models.students import Student
from lms.models.teachers import Teacher


class Punishment(models.Model):

    class Type(models.TextChoices):
        PUNISHMENT = "PU", "Взыскание"
        REBUKE = "RE", "Выговор"

    type = models.CharField(
        max_length=2,
        choices=Type.choices,
    )
    student = models.ForeignKey(
        to=Student,
        on_delete=models.CASCADE,
    )
    teacher = models.ForeignKey(
        to=Teacher,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    reason = models.CharField(max_length=200)
    date = models.DateField(default=datetime.date.today)
    remove_date = models.DateField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Punishment Journal"
        verbose_name_plural = "Punishment Journal"

    def __str__(self):
        return f"ID = {str(self.id)}\n" \
               f"StudentID = {str(self.student)}, " \
               f"TeacherID = {str(self.teacher)}\n" \
               f"Type = {str(self.type)}\n" \
               f"Date = {str(self.date)}, " \
               f"Remove Date = {str(self.remove_date)}"
