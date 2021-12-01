from django.contrib import admin

from ams.models.applicants import (
    ApplicationProcess,
    Applicant,
)

# Applicants.
admin.site.register(ApplicationProcess)
admin.site.register(Applicant)
