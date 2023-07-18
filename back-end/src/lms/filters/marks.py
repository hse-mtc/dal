from django_filters.rest_framework import (
    FilterSet,
    NumberFilter,
    BooleanFilter,
)

from lms.models.marks import (
    Mark,
    HistoricalMark,
)


class MarkFilter(FilterSet):
    milgroup = NumberFilter(field_name="student__milgroup__id")

    archived = BooleanFilter(field_name="student__milgroup__archived")

    year_of_admission = NumberFilter(method="filter_by_admission")

    def filter_by_admission(self, queryset, name, value):
        # pylint: disable=unused-argument
        value = value % 100  # strip first two symbols of the year
        return queryset.filter(student__milgroup__title__startswith=value)

    class Meta:
        model = Mark
        fields = ["student", "lesson", "archived"]


class MarkHistoryFilter(FilterSet):
    milgroup = NumberFilter(field_name="student__milgroup__id")

    archived = BooleanFilter(field_name="student__milgroup__archived")

    class Meta:
        model = HistoricalMark
        fields = ["student", "lesson", "archived"]
