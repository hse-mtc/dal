from django.contrib import admin

from common.models.subjects import Subject

from common.models.personal import (
    BirthInfo,
    ContactInfo,
    Passport,
    Photo,
    Relative,
)

# Subjects
admin.site.register(Subject)

# Personal
admin.site.register(BirthInfo)
admin.site.register(ContactInfo)
admin.site.register(Passport)
admin.site.register(Photo)
admin.site.register(Relative)
