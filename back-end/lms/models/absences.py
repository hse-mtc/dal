import datetime

from django.db import models

from lms.models.students import Student


class Absence(models.Model):

    class AbsenceType(models.TextChoices):
        SERIOUS = 'SE', 'Уважительная'
        NOT_SERIOUS = 'NS', 'Неуважительная'
        LATE = 'LA', 'Опоздание'

    class AbsenceStatus(models.TextChoices):
        OPEN = 'OP', 'Открыт'
        CLOSED = 'CL', 'Закрыт'

    date = models.DateField(default=datetime.date.today)
    student = models.ForeignKey(Student, models.CASCADE)
    absence_type = models.CharField(max_length=2, choices=AbsenceType.choices)
    absence_status = models.CharField(max_length=2, choices=AbsenceStatus.choices)
    reason = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Date = {str(self.date)}\n' \
               f'StudentID = {str(self.student)}, ' \
               f'Absence type={str(self.absence_type)}\n'

    class Meta:
        unique_together = (('date', 'student'),)
        verbose_name = 'Absence Journal'
        verbose_name_plural = 'Absence Journal'


class AbsenceTime(models.Model):
    absence_restriction_time = models.TimeField()

    def __str__(self):
        return self.absence_restriction_time

    class Meta:
        verbose_name = 'Absence Time'
        verbose_name_plural = 'Abcense Time'
