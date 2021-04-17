from django.db import models

from common.models.persons import (
    Personnel,
    Relative,
)

from lms.models.common import (
    Milgroup,
    Milspecialty,
)

from lms.models.universities import UniversityInfo
from lms.models.applicants import ApplicationProcess


class Passport(models.Model):
    series = models.CharField(max_length=4)
    code = models.CharField(max_length=6)
    ufms_name = models.CharField(max_length=255)
    ufms_code = models.CharField(max_length=7)
    issue_date = models.DateField()

    class Meta:
        verbose_name = 'Passport'
        verbose_name_plural = 'Passports'


class RecruitmentOffice(models.Model):
    title = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=127, blank=True)
    district = models.CharField(max_length=127, blank=True)

    class Meta:
        verbose_name = 'Recruitment Office'
        verbose_name_plural = 'Recruitment Offices'


class Student(Personnel):

    class Status(models.TextChoices):
        APPLICANT = 'AP', 'абитуриент'
        STUDENT = 'ST', 'обучающийся'
        EXPELLED = 'EX', 'отчислен'
        GRADUATED = 'GR', 'выпустился'
        AWAITING = 'AW', 'в ожидании'
        DECLINED = 'DE', 'отклонен'

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.APPLICANT.value,
    )

    milgroup = models.ForeignKey(
        to=Milgroup,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    milspecialty = models.ForeignKey(
        to=Milspecialty,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    passport = models.OneToOneField(
        to=Passport,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    family = models.ManyToManyField(to=Relative, blank=True)
    recruitment_office = models.ForeignKey(
        to=RecruitmentOffice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    university_info = models.ForeignKey(
        to=UniversityInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    application_process = models.OneToOneField(
        to=ApplicationProcess,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f'ID = {self.id}, full name = {self.full_name}'
