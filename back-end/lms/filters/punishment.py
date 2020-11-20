from django_filters.rest_framework import (FilterSet, ModelChoiceFilter,
                                           DateFilter, NumberFilter)

from lms.models.student import Student
from lms.models.teacher import Teacher
from lms.models.punishment import PunishmentType, Punishment


class PunishmentFilterSet(FilterSet):
    student = ModelChoiceFilter(field_name='student',
                                queryset=Student.objects.all())
    teacher = ModelChoiceFilter(field_name='teacher',
                                queryset=Teacher.objects.all())
    punishment_type = ModelChoiceFilter(field_name='punishment_type',
                                        queryset=PunishmentType.objects.all())

    milgroup = NumberFilter(field_name='student__milgroup__milgroup')

    date_from = DateFilter(field_name='date', lookup_expr='gte')
    date_to = DateFilter(field_name='date', lookup_expr='lte')

    remove_date_from = DateFilter(field_name='remove_date', lookup_expr='gte')
    remove_date_to = DateFilter(field_name='remove_date', lookup_expr='lte')

    class Meta:
        model = Punishment
        fields = ['reason', 'milgroup']
