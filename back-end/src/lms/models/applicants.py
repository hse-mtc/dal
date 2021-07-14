from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)


class Passport(models.Model):
    series = models.CharField(max_length=4)
    code = models.CharField(max_length=6)
    ufms_name = models.CharField(max_length=255)
    ufms_code = models.CharField(max_length=7)
    issue_date = models.DateField()

    class Meta:
        verbose_name = "Passport"
        verbose_name_plural = "Passports"


class RecruitmentOffice(models.Model):
    title = models.CharField(
        max_length=255,
        blank=True,
    )
    city = models.CharField(
        max_length=127,
        blank=True,
    )
    district = models.CharField(
        max_length=127,
        blank=True,
    )

    class Meta:
        verbose_name = "Recruitment Office"
        verbose_name_plural = "Recruitment Offices"


class ApplicationProcess(models.Model):

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

    mean_grade = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0),
                    MaxValueValidator(10)],
    )

    class Meta:
        verbose_name = "Application Process"
        verbose_name_plural = "Application Processes"

    def __str__(self) -> str:
        if hasattr(self, "student"):
            return f"({self.student.id}) {self.student.full_name}"

        return f"[{self.id}]"
