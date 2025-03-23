from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from common.models.milspecialties import Milspecialty
from common.models.subjects import Subject

from common.models.personal import (
    BirthInfo,
    ContactInfo,
    Passport,
    PersonalDocumentsInfo,
    Photo,
    Relative,
)

from common.models.universities import UniversityInfo, Program, Faculty
from common.models.recruitment_office import RecruitmentOffice
from common.serializers.recruitment_office import RecruitmentOfficeResource

# Subjects
admin.site.register(Subject)

# Personal
admin.site.register(BirthInfo)
admin.site.register(ContactInfo)
admin.site.register(Passport)
admin.site.register(PersonalDocumentsInfo)
admin.site.register(Photo)
admin.site.register(Relative)

# University
admin.site.register(UniversityInfo)
admin.site.register(Program)
admin.site.register(Faculty)

# Milspecialty
admin.site.register(Milspecialty)

# Recruitment office
@admin.register(RecruitmentOffice)
class RecruitmentOfficeAdmin(ImportExportModelAdmin):
    resource_class = RecruitmentOfficeResource
    search_fields = ('city', 'name')

    def get_export_queryset(self, request):
        return self.get_queryset(request)
