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
    city = models.CharField(max_length=32)
    district = models.CharField(max_length=32)

    class Meta:
        verbose_name = 'Recruitment Office'
        verbose_name_plural = 'Recruitment Offices'


class Student(Personnel):

    class Status(models.TextChoices):
        APPLICANT = 'AP', 'абитуриент'
        STUDENT = 'ST', 'обучающийся'
        DEDUCTED = 'DE', 'отчислен'
        GRADUATED = 'GR', 'выпустился'

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.APPLICANT.value,
    )

    milgroup = models.ForeignKey(
        to=Milgroup,
        on_delete=models.DO_NOTHING,
    )
    milspecialty = models.ForeignKey(
        to=Milspecialty,
        on_delete=models.DO_NOTHING,
    )

    passport = models.OneToOneField(to=Passport, on_delete=models.DO_NOTHING)
    family = models.ManyToManyField(to=Relative)
    recruitment_office = models.ForeignKey(
        to=RecruitmentOffice,
        on_delete=models.SET_NULL,
        null=True,
    )
    university_info = models.ForeignKey(
        to=UniversityInfo,
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f'ID = {self.id}, full name = {self.full_name}'
