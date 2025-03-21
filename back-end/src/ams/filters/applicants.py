from django_filters.rest_framework import (
    FilterSet,
    ChoiceFilter,
    CharFilter,
    NumberFilter,
    BooleanFilter,
)

from common.models.universities import Campus
from common.models.military import MilitaryOffice

from ams.models.applicants import Applicant


class ApplicantFilter(FilterSet):
    campus = ChoiceFilter(
        choices=Campus.choices,
        method="filter_by_campus",
    )
    program_code = CharFilter(field_name="university_info__program__code")
    mtc_admission_year = NumberFilter(
        field_name="application_process__mtc_admission_year"
    )
    military_office = CharFilter(field_name="military_office__name")
    has_custom_military_office = BooleanFilter(field_name="custom_military_office", 
                                              lookup_expr="isnull", 
                                              exclude=True)

    def filter_by_campus(self, queryset, name, value):
        # pylint: disable=unused-argument
        return queryset.filter(university_info__program__faculty__campus=value)

    class Meta:
        model = Applicant
        fields = ["campus", "program_code", "mtc_admission_year", "military_office", "has_custom_military_office"]
