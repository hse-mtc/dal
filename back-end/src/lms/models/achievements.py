from django.db import models

from lms.models.students import Student


class AchievementType(models.Model):
    title = models.CharField(
        unique=True,
        max_length=255,
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Achievement Type"
        verbose_name_plural = "Achievement Types"


class Achievement(models.Model):
    student = models.ForeignKey(
        to=Student,
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        to=AchievementType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    text = models.TextField()
    date = models.DateField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"ID = {str(self.id)}\n" \
               f"StudentID = {str(self.student)}, " \
               f"Type = {str(self.type)}\n" \
               f"Date = {str(self.date)}"

    class Meta:
        verbose_name = "Achievement Journal"
        verbose_name_plural = "Achievement Journal"
