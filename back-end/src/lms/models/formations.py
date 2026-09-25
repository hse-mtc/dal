from django.conf import settings
from django.db import models
from django.db.models import F, Q

from lms.models.common import Milgroup
from lms.models.students import Student


class FormationReport(models.Model):
    milgroup = models.ForeignKey(Milgroup, on_delete=models.RESTRICT)
    date = models.DateField()
    roster_count = models.PositiveIntegerField()
    present_count = models.PositiveIntegerField()
    excused_count = models.PositiveIntegerField()
    unexcused_count = models.PositiveIntegerField()
    unknown_count = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_formation_reports",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="updated_formation_reports",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("milgroup", "date")]
        constraints = [
            models.CheckConstraint(
                check=Q(
                    roster_count=F("present_count")
                    + F("excused_count")
                    + F("unexcused_count")
                    + F("unknown_count")
                ),
                name="formation_counts_match_roster",
            ),
        ]


class FormationRemark(models.Model):
    class Category(models.TextChoices):
        HAIRCUT = "HC", "Не стрижен"
        UNIFORM = "UN", "Нарушение формы одежды"
        LATE = "LA", "Опоздал к построению"
        OTHER = "OT", "Другое"

    report = models.ForeignKey(
        FormationReport, on_delete=models.CASCADE, related_name="remarks"
    )
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    student_name = models.CharField(max_length=200)
    category = models.CharField(max_length=2, choices=Category.choices)
    comment = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
