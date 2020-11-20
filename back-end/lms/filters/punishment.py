from django_filters.rest_framework import (FilterSet,
                                           DateFilter,
                                           NumberFilter)

from lms.models.punishment import Punishment


class PunishmentFilter(FilterSet):

    milgroup = NumberFilter(field_name='student__milgroup__milgroup')

    date_from = DateFilter(field_name='date', lookup_expr='gte')
    date_to = DateFilter(field_name='date', lookup_expr='lte')

    remove_date_from = DateFilter(field_name='remove_date', lookup_expr='gte')
    remove_date_to = DateFilter(field_name='remove_date', lookup_expr='lte')

    class Meta:
        model = Punishment
        fields = ['reason', 'milgroup', 'student', 'teacher',
                  'punishment_type']
