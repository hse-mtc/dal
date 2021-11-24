from django_filters.rest_framework import (
    FilterSet,
    CharFilter,
    BooleanFilter,
    NumberFilter,
)

from lms.models.common import Milgroup


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
