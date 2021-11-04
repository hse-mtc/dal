from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)

from lms.models.lessons import Lesson
from lms.models.students import Student


class Mark(models.Model):
    values = ArrayField(base_field=models.IntegerField(
        validators=[MaxValueValidator(5),
                    MinValueValidator(2)]))
    lesson = models.ForeignKey(
        to=Lesson,
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        to=Student,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Mark"
        verbose_name_plural = "Marks"
        unique_together = [["lesson", "student"]]

    def __str__(self):
        return f"Marks {self.values} for StudentID=" \
               f"{self.student} on LessonID={self.lesson}"
