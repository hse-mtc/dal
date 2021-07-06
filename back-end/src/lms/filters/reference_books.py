from django_filters.rest_framework import (
    FilterSet,
    ChoiceFilter,
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

    archived = BooleanFilter(field_name="archived")

    year_of_admission = NumberFilter(method="filter_by_admission")

    def filter_by_admission(self, queryset, name, value):
        # pylint: disable=unused-argument
        value = str(value).split("20")[1]  # strip first two symbols of the year
        return queryset.filter(milgroup__startswith=value)

    class Meta:
        model = Milgroup
        fields = "__all__"


class ProgramFilter(FilterSet):

    class Meta:
        model = Program
        fields = "__all__"
