from django_filters.rest_framework import (FilterSet, DateFilter, NumberFilter)

from lms.models.absence import Absence


class AbsenceFilter(FilterSet):

    milgroup = NumberFilter(field_name='student__milgroup__milgroup')

    date_from = DateFilter(field_name='date', lookup_expr='gte')
    date_to = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Absence
        fields = ['milgroup', 'student', 'absence_type', 'absence_status']
