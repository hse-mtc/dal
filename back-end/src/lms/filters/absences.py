from django_filters.rest_framework import (
    FilterSet,
    DateFilter,
    NumberFilter,
    BooleanFilter,
)

from lms.models.absences import Absence


class AbsenceFilter(FilterSet):

    milgroup = NumberFilter(field_name='student__milgroup__milgroup')

    date_from = DateFilter(field_name='date', lookup_expr='gte')
    date_to = DateFilter(field_name='date', lookup_expr='lte')

    archived = BooleanFilter(field_name='student__milgroup__archived')

    year_of_admission = NumberFilter(method='filter_by_admission')

    def filter_by_admission(self, queryset, name, value):
        # pylint: disable=unused-argument
        value = value % 100  # strip first two symbols of the year
        return queryset.filter(student__milgroup__milgroup__startswith=value)

    class Meta:
        model = Absence
        fields = ['milgroup', 'student', 'type', 'status', 'archived']
