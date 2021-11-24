from django.db import models
from django.contrib.auth import get_user_model

from common.models.universities import UniversityInfo
from common.models.personal import (
    BirthInfo,
    ContactInfo,
    Passport,
    Photo,
    Relative,
)

from ams.models.applicants import Applicant

from lms.models.common import (
    Milfaculty,
    Milgroup,
)


class Skill(models.Model):
    title = models.CharField(
        unique=True,
        max_length=255,
    )

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self) -> str:
        return self.title


class Student(models.Model):

    # --------------------------------------------------------------------------

    class Status(models.TextChoices):
        ENROLLED = "EN", "Зачислен"
        STUDYING = "ST", "Обучается"
        EXPELLED = "EX", "Отчислен"
        GRADUATED = "GR", "Выпустился"

    class Post(models.TextChoices):
        MILGROUP_COMMANDER = "GC", "Командир взвода"
        MILSQUAD_COMMANDER = "SC", "Командир отделения"

    # --------------------------------------------------------------------------
    # Frequently accessed data.

    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    patronymic = models.CharField(
        max_length=64,
        blank=True,
    )
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    milgroup = models.ForeignKey(
        to=Milgroup,
        # TODO(TmLev): What if `milgroup` needs to be deleted?
        on_delete=models.RESTRICT,
    )
    contact_info = models.OneToOneField(
        to=ContactInfo,
        on_delete=models.RESTRICT,
    )

    # --------------------------------------------------------------------------
    # Rarely accessed studying data.

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
    )
    post = models.CharField(
        max_length=2,
        choices=Post.choices,
        default=None,
        null=True,
        blank=True,
    )
    skills = models.ManyToManyField(
        to=Skill,
        blank=True,
    )

    # --------------------------------------------------------------------------
    # Rarely accessed personal data.

    photo = models.OneToOneField(
        to=Photo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    birth_info = models.OneToOneField(
        to=BirthInfo,
        on_delete=models.RESTRICT,
    )
    citizenship = models.CharField(
        max_length=64,
        blank=True,
    )
    permanent_address = models.CharField(
        max_length=128,
        blank=True,
    )
    passport = models.OneToOneField(
        to=Passport,
        on_delete=models.RESTRICT,
    )
    recruitment_office = models.CharField(max_length=255)
    university_info = models.OneToOneField(
        to=UniversityInfo,
        on_delete=models.RESTRICT,
    )
    family = models.ManyToManyField(
        to=Relative,
        blank=True,
    )

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"[{self.id}] {self.fullname}"

    @property
    def fullname(self) -> str:
        return " ".join([self.surname, self.name, self.patronymic])

    @property
    def milfaculty(self) -> Milfaculty:
        return self.milgroup.milfaculty

    @staticmethod
    def from_applicant(
        applicant: Applicant,
        milgroup: Milgroup,
    ) -> "Student":
        student = Student.objects.create(
            surname=applicant.surname,
            name=applicant.name,
            patronymic=applicant.patronymic,
            # TODO(TmLev): When is the user created? Maybe here?
            milgroup=milgroup,
            contact_info=applicant.contact_info,
            status=Student.Status.ENROLLED.value,
            photo=applicant.photo,
            birth_info=applicant.birth_info,
            citizenship=applicant.citizenship,
            permanent_address=applicant.permanent_address,
            passport=applicant.passport,
            recruitment_office=applicant.recruitment_office,
            university_info=applicant.university_info,
        )
        student.family.add(*applicant.family.order_by("id"))
        student.save()
        return student


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

    def __str__(self) -> str:
        return f"[{self.id}] {self.student.fullname} / {self.student.id}"
