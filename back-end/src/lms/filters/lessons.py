from django_filters.rest_framework import (
    FilterSet,
    NumberFilter,
    DateFilter,
    BooleanFilter,
)

from lms.models.lessons import Lesson


class LessonFilter(FilterSet):
    milgroup = NumberFilter(field_name="milgroup__id")

    date_from = DateFilter(field_name="date", lookup_expr="gte")
    date_to = DateFilter(field_name="date", lookup_expr="lte")

    archived = BooleanFilter(field_name="milgroup__archived")

    year_of_admission = NumberFilter(method="filter_by_admission")

    def filter_by_admission(self, queryset, name, value):
        # pylint: disable=unused-argument
        value = value % 100  # strip first two symbols of the year
        return queryset.filter(milgroup__title__startswith=value)

    class Meta:
        model = Lesson
        fields = ["ordinal"]
