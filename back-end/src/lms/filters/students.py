from django_filters.rest_framework import (
    FilterSet,
    ChoiceFilter,
    CharFilter,
    BooleanFilter,
    NumberFilter,
)

from lms.models.students import Student
from lms.models.universities import UniversityInfo


class StudentFilter(FilterSet):
    campus = ChoiceFilter(
        choices=UniversityInfo.Campus.choices,
        method="filter_by_campus",
    )

    # TODO(TmLev): consider different formats, strip +7/8/7 from beginning.
    phone = CharFilter(field_name="contact_info__personal_phone_number")

    program = CharFilter(field_name="university_info__program__code")
    student_skill = CharFilter(field_name="student_skills__title",
                               lookup_expr="icontains")
    archived = BooleanFilter(field_name="milgroup__archived")
    year_of_admission = NumberFilter(method="filter_by_admission")

    def filter_by_admission(self, queryset, name, value):
        # pylint: disable=unused-argument
        value = str(value).split("20")[1]  # strip first two symbols of the year
        return queryset.filter(milgroup__milgroup__startswith=value)

    def filter_by_campus(self, queryset, name, value):
        # pylint: disable=unused-argument
        return queryset.filter(university_info__campus=value)

    class Meta:
        model = Student
        fields = ["status", "milgroup", "campus", "student_skill", "archived"]
