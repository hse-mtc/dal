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
    list_select_related = ["applicant"]
    ordering = ["id"]
    search_fields = [
        "=id",
        "applicant__surname",
        "applicant__name",
        "applicant__patronymic",
        "applicant__user__email",
    ]
    show_full_result_count = False
    readonly_fields = [
        "strength_score",
        "speed_score",
        "endurance_score",
        "physical_test_grade",
    ]


class ApplicantAdmin(admin.ModelAdmin):
    autocomplete_fields = ["application_process"]
    list_display = [
        "id",
        "surname",
        "name",
        "patronymic",
        "corporate_email",
        "program_code",
        "campus",
        "admission_year",
        "milspecialty",
    ]
    list_filter = [
        "application_process__mtc_admission_year",
        "university_info__program__faculty__campus",
        "milspecialty",
        "marital_status",
    ]
    list_select_related = [
        "application_process",
        "contact_info",
        "milspecialty",
        "university_info__program__faculty",
    ]
    ordering = ["surname", "name", "patronymic", "id"]
    raw_id_fields = [
        "birth_info",
        "passport",
        "personal_documents_info",
        "university_info",
        "contact_info",
        "photo",
        "video",
        "family",
        "user",
    ]
    search_fields = [
        "surname",
        "name",
        "patronymic",
        "contact_info__corporate_email",
        "user__email",
        "university_info__program__code",
    ]
    show_full_result_count = False

    @admin.display(ordering="contact_info__corporate_email")
    def corporate_email(self, applicant):
        return applicant.contact_info.corporate_email

    @admin.display(ordering="university_info__program__code")
    def program_code(self, applicant):
        return applicant.university_info.program.code

    @admin.display(ordering="university_info__program__faculty__campus")
    def campus(self, applicant):
        return applicant.university_info.program.faculty.get_campus_display()

    @admin.display(ordering="application_process__mtc_admission_year")
    def admission_year(self, applicant):
        return applicant.application_process.mtc_admission_year

    def get_search_results(self, request, queryset, search_term):
        if search_term.isdigit():
            return queryset.filter(pk=int(search_term)), False
        return super().get_search_results(request, queryset, search_term)


# Applicants.
admin.site.register(ApplicationProcess, ApplicationProcessAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(ExerciseResult)
