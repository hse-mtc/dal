from django.db import models
from django.contrib.auth import get_user_model

from common.models.persons import (
    Personnel,
    Relative,
)

from lms.models.common import (
    Milgroup,
    Milspecialty,
)

from lms.models.universities import UniversityInfo
from lms.models.applicants import (
    Passport,
    RecruitmentOffice,
    ApplicationProcess,
)


class Skill(models.Model):
    title = models.CharField(
        unique=True,
        max_length=255,
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"


class Student(Personnel):

    class Status(models.TextChoices):
        APPLICANT = "AP", "абитуриент"
        STUDENT = "ST", "обучающийся"
        EXPELLED = "EX", "отчислен"
        GRADUATED = "GR", "выпустился"
        AWAITING = "AW", "в ожидании"
        DECLINED = "DE", "отклонен"

    class Post(models.TextChoices):
        MILGROUP_COMMANDER = "GC", "командир взвода"
        MILSQUAD_COMMANDER = "SC", "командир отделения"

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.APPLICANT.value,
    )
    post = models.CharField(
        max_length=2,
        choices=Post.choices,
        default=None,
        null=True,
        blank=True,
    )

    milgroup = models.ForeignKey(
        to=Milgroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    milspecialty = models.ForeignKey(
        to=Milspecialty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    skills = models.ManyToManyField(
        to=Skill,
        blank=True,
    )

    passport = models.OneToOneField(
        to=Passport,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    family = models.ManyToManyField(
        to=Relative,
        blank=True,
    )
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
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"ID = {self.id}, full name = {self.full_name}"


class Note(models.Model):
    text = models.TextField()
    # author of the note
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        to=Student,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
