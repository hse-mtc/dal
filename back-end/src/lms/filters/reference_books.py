from django_filters.rest_framework import (
    FilterSet,
    ChoiceFilter,
    CharFilter,
    BooleanFilter,
    NumberFilter,
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
    archived = BooleanFilter()

    title = CharFilter(lookup_expr="icontains")

    year_of_admission = NumberFilter(method="filter_by_admission")

    def filter_by_admission(self, queryset, name, value):
        # pylint: disable=unused-argument
        value = value % 100  # strip first two symbols of the year
        return queryset.filter(title__startswith=value)

    class Meta:
        model = Milgroup
        fields = "__all__"


class ProgramFilter(FilterSet):

    class Meta:
        model = Program
        fields = "__all__"
