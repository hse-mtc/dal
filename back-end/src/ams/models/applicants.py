from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)

from common.models.universities import UniversityInfo
from common.models.milspecialties import Milspecialty
from common.models.personal import (
    BirthInfo,
    ContactInfo,
    Passport,
    Photo,
    Relative,
)


class ApplicationProcess(models.Model):

    # --------------------------------------------------------------------------

    # TODO(TmLev): replace russian labels with english?..
    class MedicalExamination(models.TextChoices):
        FIT = "FI", "годен"
        FIT_MINOR_RESTRICTIONS = "FMR", "годен с незначительными ограничениями"
        FIT_LIMITED = "FLI", "ограниченно годен"
        UNFIT_RESTRICTEDLY = "UR", "ограниченно не годен"
        UNFIT = "UN", "не годен"

    class ProfPsySelection(models.TextChoices):
        FIRST = "FI", "I"
        SECOND = "SE", "II"
        THIRD = "TH", "III"
        FOURTH = "FO", "IV"

    # --------------------------------------------------------------------------

    milspecialty = models.ForeignKey(
        to=Milspecialty,
        on_delete=models.RESTRICT,
    )

    mean_grade = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )

    medical_examination = models.CharField(
        max_length=3,
        choices=MedicalExamination.choices,
        blank=True,
    )
    prof_psy_selection = models.CharField(
        max_length=2,
        choices=ProfPsySelection.choices,
        blank=True,
    )

    preferential_right = models.BooleanField(default=False)
    characteristic_handed_over = models.BooleanField(default=False)
    criminal_record_handed_over = models.BooleanField(default=False)
    passport_handed_over = models.BooleanField(default=False)
    registration_certificate_handed_over = models.BooleanField(default=False)
    university_card_handed_over = models.BooleanField(default=False)
    application_handed_over = models.BooleanField(default=False)

    # Number of pull ups.
    pull_ups = models.SmallIntegerField(
        default=None,
        null=True,
        blank=True,
    )
    # In seconds.
    speed_run = models.FloatField(
        default=None,
        null=True,
        blank=True,
    )
    # In minutes.
    long_run = models.FloatField(
        default=None,
        null=True,
        blank=True,
    )
    physical_test_grade = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = "Application Process"
        verbose_name_plural = "Application Processes"

    def __str__(self) -> str:
        return f"[{self.id}] {self.applicant.fullname} / {self.applicant.id}"


class Applicant(models.Model):
    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    patronymic = models.CharField(
        max_length=64,
        blank=True,
    )
    recruitment_office = models.CharField(max_length=255)
    citizenship = models.CharField(
        max_length=64,
        blank=True,
    )
    permanent_address = models.CharField(
        max_length=128,
        blank=True,
    )
    birth_info = models.OneToOneField(
        to=BirthInfo,
        on_delete=models.RESTRICT,
    )
    passport = models.OneToOneField(
        to=Passport,
        on_delete=models.RESTRICT,
    )
    university_info = models.OneToOneField(
        to=UniversityInfo,
        on_delete=models.RESTRICT,
    )
    contact_info = models.OneToOneField(
        to=ContactInfo,
        on_delete=models.RESTRICT,
    )
    photo = models.OneToOneField(
        to=Photo,
        on_delete=models.SET_NULL,
        null=True,
    )
    family = models.ManyToManyField(
        to=Relative,
        blank=True,
    )
    # `Applicant` must always have `ApplicationProcess`.
    application_process = models.OneToOneField(
        to=ApplicationProcess,
        on_delete=models.RESTRICT,
    )

    class Meta:
        verbose_name = "Applicant"
        verbose_name_plural = "Applicants"

    def __str__(self):
        return f"[{self.id}] {self.fullname}"

    @property
    def fullname(self) -> str:
        return " ".join([self.surname, self.name, self.patronymic])
