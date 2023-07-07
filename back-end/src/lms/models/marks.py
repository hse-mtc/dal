from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from simple_history.models import HistoricalRecords

from lms.models.lessons import Lesson
from lms.models.students import Student


class Mark(models.Model):
    values = ArrayField(
        base_field=models.IntegerField(
            validators=[MaxValueValidator(5), MinValueValidator(2)]
        )
    )
    lesson = models.ForeignKey(
        to=Lesson,
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        to=Student,
        on_delete=models.CASCADE,
    )
    history = HistoricalRecords()
    changed_by = models.ForeignKey(
        to=get_user_model(), on_delete=models.CASCADE, null=True
    )

    class Meta:
        verbose_name = "Mark"
        verbose_name_plural = "Marks"
        unique_together = [["lesson", "student"]]

    def __str__(self):
        return (
            f"Marks {self.values} for StudentID="
            f"{self.student} on LessonID={self.lesson}"
        )

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
