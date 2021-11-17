from django_filters.rest_framework import (
    FilterSet,
    ChoiceFilter,
)

from common.models.universities import Program, Campus


class ProgramFilter(FilterSet):
    campus = ChoiceFilter(
        choices=Campus.choices,
        method="filter_by_campus",
    )

    def filter_by_campus(self, queryset, name, value):
        # pylint: disable=unused-argument
        return queryset.filter(faculty__campus=value)

    class Meta:
        model = Program
        fields = ["campus"]
