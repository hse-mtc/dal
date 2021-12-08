from django.contrib import admin

from ams.models.applicants import (
    ApplicationProcess,
    Applicant,
)
from ams.models.staff import Staff

# Applicants.

admin.site.register(ApplicationProcess)
admin.site.register(Applicant)
admin.site.register(Staff)
