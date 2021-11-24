import datetime

from django.db import models

from lms.models.students import Student
from lms.models.teachers import Teacher


class Encouragement(models.Model):

    class Type(models.TextChoices):
        ENCOURAGEMENT = "EN", "Благодарность"
        REMOVE_PUNISHMENT = "RE", "Снятие взыскания"

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
    reason = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name = "Encouragement Journal"
        verbose_name_plural = "Encouragement Journal"

    def __str__(self):
        return f"ID = {str(self.id)}\n" \
               f"StudentID = {str(self.student)}, " \
               f"TeacherID = {str(self.teacher)}\n" \
               f"Type = {str(self.type)}\n" \
               f"Date = {str(self.date)}"
