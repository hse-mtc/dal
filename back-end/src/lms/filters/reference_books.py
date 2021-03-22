from django_filters.rest_framework import (
    FilterSet,
    ChoiceFilter,
)

from lms.models.universities import (
    UniversityInfo,
    Program,
)
from lms.models.common import (
    Milgroup,
    Milspecialty,
)


class MilspecialtyFilter(FilterSet):
    campus = ChoiceFilter(
        choices=UniversityInfo.Campus.choices,
        method="filter_by_campus",
    )

    def filter_by_campus(self, queryset, name, value):
        # pylint: disable=unused-argument
        return queryset.filter(available_for__contains=[value])

    class Meta:
        model = Milspecialty
        fields = ["campus"]


class MilgroupFilter(FilterSet):

    class Meta:
        model = Milgroup
        fields = "__all__"


class ProgramFilter(FilterSet):

    class Meta:
        model = Program
        fields = "__all__"
