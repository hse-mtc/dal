from django_filters.rest_framework import (
    FilterSet,
    ChoiceFilter,
)

from lms.models.students import Student
from lms.models.universities import UniversityInfo


class StudentFilter(FilterSet):
    campus = ChoiceFilter(
        choices=UniversityInfo.Campus.choices,
        method="filter_by_campus",
    )

    def filter_by_campus(self, queryset, name, value):
        # pylint: disable=unused-argument
        return queryset.filter(university_info__campus=value)

    class Meta:
        model = Student
        fields = ['status', 'milgroup', 'campus']
