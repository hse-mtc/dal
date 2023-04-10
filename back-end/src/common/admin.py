from django.contrib import admin

from common.models.milspecialties import Milspecialty
from common.models.subjects import Subject

from common.models.personal import (
    BirthInfo,
    ContactInfo,
    Passport,
    Photo,
    Relative,
)

from common.models.universities import UniversityInfo, Program, Faculty

# Subjects
admin.site.register(Subject)

# Personal
admin.site.register(BirthInfo)
admin.site.register(ContactInfo)
admin.site.register(Passport)
admin.site.register(Photo)
admin.site.register(Relative)

# University
admin.site.register(UniversityInfo)
admin.site.register(Program)
admin.site.register(Faculty)

# Milspeciality
admin.site.register(Milspecialty)
