from django.contrib import admin

from ams.models.applicants import (
    RecruitmentOffice,
    ApplicationProcess,
    Applicant,
)

# Applicants.
admin.site.register(RecruitmentOffice)
admin.site.register(ApplicationProcess)
admin.site.register(Applicant)
