from django_filters.rest_framework import (FilterSet, NumberFilter,
                                           BooleanFilter, NumberFilter,)

from lms.models.marks import Mark


class MarkFilter(FilterSet):
    milgroup = NumberFilter(field_name='student__milgroup__milgroup')

    archived = BooleanFilter(field_name='student__milgroup__archived')

    year_of_admission = NumberFilter(method="filter_by_admission")

    def filter_by_admission(self, queryset, name, value):
        # pylint: disable=unused-argument
        value = value % 100  # strip first two symbols of the year
        return queryset.filter(student__milgroup__milgroup__startswith=value)

    class Meta:
        model = Mark
        fields = ['student', 'lesson', 'archived']
