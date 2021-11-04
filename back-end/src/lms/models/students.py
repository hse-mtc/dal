from django.db import models
from django.contrib.auth import get_user_model

from common.models.universities import UniversityInfo
from common.models.personal import (
    BirthInfo,
    ContactInfo,
    Name,
    Photo,
    Relative,
)

from ams.models.applicants import (
    Applicant,
    Passport,
    RecruitmentOffice,
)

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
        ENROLLED = "EN", "зачислен"
        STUDYING = "ST", "обучается"
        EXPELLED = "EX", "отчислен"
        GRADUATED = "GR", "выпустился"

    class Post(models.TextChoices):
        MILGROUP_COMMANDER = "GC", "командир взвода"
        MILSQUAD_COMMANDER = "SC", "командир отделения"

    # --------------------------------------------------------------------------
    # Frequently accessed data.

    name = models.ForeignKey(
        to=Name,
        on_delete=models.RESTRICT,
    )
    user = models.ForeignKey(
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
    contact_info = models.ForeignKey(
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

    photo = models.ForeignKey(
        to=Photo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    birth_info = models.ForeignKey(
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
    passport = models.ForeignKey(
        to=Passport,
        on_delete=models.RESTRICT,
    )
    recruitment_office = models.ForeignKey(
        to=RecruitmentOffice,
        on_delete=models.RESTRICT,
    )
    university_info = models.ForeignKey(
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
        return f"[{self.id}] {self.name}"

    @staticmethod
    def from_applicant(
        applicant: Applicant,
        milgroup: Milgroup,
    ) -> "Student":
        student = Student.objects.create(
            name=applicant.name,
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

    @property
    def milfaculty(self) -> Milfaculty:
        return self.milgroup.milfaculty


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
        return f"[{self.id}] {self.student.name} / {self.student.id}"
