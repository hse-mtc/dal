from django.contrib import admin

from ams.models.applicants import (
    Applicant,
    ApplicationProcess,
)
from ams.models.physical import ExerciseResult


class ExerciseResultInline(admin.TabularInline):
    model = ExerciseResult
    extra = 0
    readonly_fields = ["secondary_score"]


class ApplicationProcessAdmin(admin.ModelAdmin):
    inlines = [ExerciseResultInline]
    readonly_fields = [
        "strength_score",
        "speed_score",
        "endurance_score",
        "physical_test_grade",
    ]


# Applicants.
admin.site.register(ApplicationProcess, ApplicationProcessAdmin)
admin.site.register(Applicant)
admin.site.register(ExerciseResult)
