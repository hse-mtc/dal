import datetime

from django.db import models

from lms.models.student import Student


class AbsenceType(models.Model):
    absence_type = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.absence_type)

    class Meta:
        db_table = 'absence_type'
        verbose_name = 'Absence Type'
        verbose_name_plural = 'Absence Types'


class AbsenceStatus(models.Model):
    absence_status = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.absence_status)

    class Meta:
        db_table = 'absence_status'
        verbose_name = 'Absence Status'
        verbose_name_plural = 'Absence Statuses'


class Absence(models.Model):
    date = models.DateField(default=datetime.date.today)
    student = models.ForeignKey(Student, models.CASCADE, db_column='student')
    absence_type = models.ForeignKey(AbsenceType,
                                     models.DO_NOTHING,
                                     db_column='absence_type')
    absence_status = models.ForeignKey(AbsenceStatus,
                                       models.DO_NOTHING,
                                       db_column='absence_status')
    reason = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'Date = {str(self.date)}\n' \
               f'StudentID = {str(self.student)}, ' \
               f'Absence type={str(self.absence_type)}\n'

    class Meta:
        db_table = 'absence'
        unique_together = (('date', 'student'),)
        verbose_name = 'Absence Journal'
        verbose_name_plural = 'Absence Journal'
