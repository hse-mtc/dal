import datetime

from django.db import models
from django.core.validators import ValidationError

from lms.models.students import Student


class Absence(models.Model):

    class Excuse(models.TextChoices):
        LATE = "LA", "Опоздание"
        LEGITIMATE = "LE", "Уважительная"
        ILLEGITIMATE = "IL", "Неуважительная"

    class Status(models.TextChoices):
        OPEN = "OP", "Открыт"
        CLOSED = "CL", "Закрыт"

    excuse = models.CharField(
        max_length=2,
        choices=Excuse.choices,
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
    )

    date = models.DateField(default=datetime.date.today)
    reason = models.CharField(
        max_length=127,
        null=True,
        blank=True,
    )
    comment = models.CharField(
        max_length=127,
        null=True,
        blank=True,
    )
    student = models.ForeignKey(
        to=Student,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"ID = {self.id}\n" \
               f"Date = {self.date}\n" \
               f"StudentID = {self.student}, " \
               f"excuse = {self.excuse}\n"

    class Meta:
        unique_together = [("date", "student")]
        verbose_name = "Absence Journal"
        verbose_name_plural = "Absence Journal"


class AbsenceTime(models.Model):
    absence_restriction_time = models.TimeField()

    def save(self, *args, **kwargs):
        if not self.pk and AbsenceTime.objects.exists():
            raise ValidationError(
                "There can only be one instance of absence restriction time"
            )
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.absence_restriction_time.strftime("%X")

    class Meta:
        verbose_name = "Absence Time"
        verbose_name_plural = "Absence Time"
