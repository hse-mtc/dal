from django_filters.rest_framework import (
    FilterSet,
    ChoiceFilter,
    CharFilter,
)

from common.models.universities import Campus

from ams.models.applicants import Applicant


class ApplicantFilter(FilterSet):
    campus = ChoiceFilter(
        choices=Campus.choices,
        method="filter_by_campus",
    )
    program_code = CharFilter(field_name="university_info__program__code")

    def filter_by_campus(self, queryset, name, value):
        # pylint: disable=unused-argument
        return queryset.filter(university_info__program__faculty__campus=value)

    class Meta:
        model = Applicant
        fields = ["campus", "program_code"]
