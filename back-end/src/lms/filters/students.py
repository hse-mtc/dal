from django_filters.rest_framework import (
    FilterSet,
    CharFilter,
    BooleanFilter,
    NumberFilter,
)

from lms.models.students import (
    Student,
    Note,
)


class StudentFilter(FilterSet):
    # TODO(TmLev): consider different formats, strip +7/8/7 from beginning.
    phone = CharFilter(field_name="contact_info__personal_phone_number")

    milfaculty = NumberFilter(field_name="milgroup__milfaculty__id")

    skill = CharFilter(field_name="skills__title", lookup_expr="icontains")
    archived = BooleanFilter(field_name="milgroup__archived")
    year_of_admission = NumberFilter(method="filter_by_admission")

    def filter_by_admission(self, queryset, name, value):
        # pylint: disable=unused-argument
        value = value % 100  # strip first two symbols of the year
        return queryset.filter(milgroup__title__startswith=value)

    class Meta:
        model = Student
        fields = [
            "phone",
            "milfaculty",
            "skill",
            "archived",
            "year_of_admission",
            "status",
            "milgroup",
        ]


class NoteFilter(FilterSet):
    class Meta:
        model = Note
        fields = ["student"]
