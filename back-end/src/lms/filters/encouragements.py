from django_filters.rest_framework import (FilterSet, DateFilter, NumberFilter)

from lms.models.encouragements import Encouragement


class EncouragementFilter(FilterSet):

    milgroup = NumberFilter(field_name='student__milgroup__milgroup')

    date_from = DateFilter(field_name='date', lookup_expr='gte')
    date_to = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Encouragement
        fields = ['reason', 'milgroup', 'student', 'teacher', 'type']
