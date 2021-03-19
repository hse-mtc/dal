from django.contrib import admin

from common.models.subjects import Subject
from common.models.persons import (
    Relative,
    BirthInfo,
    ContactInfo,
)

admin.site.register(Subject)
admin.site.register(Relative)
admin.site.register(BirthInfo)
admin.site.register(ContactInfo)
