from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.contrib.auth import get_user_model

from ams.utils.common import get_current_admission_year
from common.models.universities import UniversityInfo
from common.models.milspecialties import Milspecialty
from common.models.personal import (
    BirthInfo,
    ContactInfo,
    Passport,
    PersonalDocumentsInfo,
    Photo,
    Relative,
)


class ApplicationProcess(models.Model):
    # --------------------------------------------------------------------------

    class MedicalExamination(models.TextChoices):
        FIT = "FI", "Годен"
        FIT_MINOR_RESTRICTIONS = "FMR", "Годен с незначительными ограничениями"
        FIT_LIMITED = "FLI", "Ограниченно годен"
        UNFIT_RESTRICTEDLY = "UR", "Ограниченно не годен"
        UNFIT = "UN", "Не годен"

    class ProfPsySelection(models.TextChoices):
        FIRST = "FI", "I"
        SECOND = "SE", "II"
        THIRD = "TH", "III"
        FOURTH = "FO", "IV"

    # --------------------------------------------------------------------------

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
    mtc_admission_year = models.IntegerField(default=0)

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
        try:
            return f"[{self.id}] {self.applicant.fullname} / {self.applicant.id}"
        except Applicant.DoesNotExist:
            return f"[{self.id}]"


class ApplicantManager(models.Manager):
    """Ensures that every Applicant has ApplicationProcess."""

    def create(self, *args, **kwargs):
        if "application_process" not in kwargs:
            app_process = ApplicationProcess.objects.create()
            app_process.mtc_admission_year = get_current_admission_year()
            app_process.save()

            kwargs["application_process"] = app_process
        return super().create(*args, **kwargs)


class Applicant(models.Model):
    class MaritalStatus(models.TextChoices):
        UNKNOWN = "UN", ""
        SINGLE = "SI", "Холост"
        MARRIED = "MA", "Женат"

    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    patronymic = models.CharField(
        max_length=64,
        blank=True,
    )
    surname_genitive = models.CharField(max_length=64)
    name_genitive = models.CharField(max_length=64)
    patronymic_genitive = models.CharField(
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
    personal_documents_info = models.OneToOneField(
        to=PersonalDocumentsInfo,
        null=True,
        blank=True,
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
    nationality = models.CharField(
        max_length=64,
        blank=False,
        default="-",
        verbose_name="Национальность",
    )
    marital_status = models.CharField(
        max_length=2,
        default=MaritalStatus.UNKNOWN,
        choices=MaritalStatus.choices,
        blank=False,
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
    # `Applicant` must always choose some `Milspecialty`.
    milspecialty = models.ForeignKey(
        to=Milspecialty,
        on_delete=models.RESTRICT,
    )
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.RESTRICT,
    )

    objects = ApplicantManager()

    class Meta:
        verbose_name = "Applicant"
        verbose_name_plural = "Applicants"

    def __str__(self):
        return f"[{self.id}] {self.fullname}"

    @property
    def fullname(self) -> str:
        return " ".join([self.surname, self.name, self.patronymic])
