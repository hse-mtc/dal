from django.db import models


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
    preferential_right = models.BooleanField(default=False,)
    characteristic_handed_over = models.BooleanField(default=False,)
    criminal_record_handed_over = models.BooleanField(default=False,)
    passport_handed_over = models.BooleanField(default=False,)
    registration_certificate_handed_over = models.BooleanField(default=False,)
    university_card_handed_over = models.BooleanField(default=False,)
    application_handed_over = models.BooleanField(default=False,)

    class Meta:
        verbose_name = "Application Process"
        verbose_name_plural = "Application Processes"

    def __str__(self) -> str:
        if hasattr(self, "student"):
            return f"({self.student.id}) {self.student.full_name}"
        else:
            return f"[{self.id}]"
