from django_filters.rest_framework import (
    FilterSet,
    ChoiceFilter,
)

from common.models.milspecialties import Milspecialty
from common.models.universities import Campus


class MilspecialtyFilter(FilterSet):
    campus = ChoiceFilter(
        choices=Campus.choices,
        method="filter_by_campus",
    )

    def filter_by_campus(self, queryset, name, value):
        # pylint: disable=unused-argument
        return queryset.filter(available_for__contains=[value])

    class Meta:
        model = Milspecialty
        fields = ["campus"]
