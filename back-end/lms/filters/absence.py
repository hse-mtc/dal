from django_filters.rest_framework import (FilterSet, ModelChoiceFilter,
                                           DateFilter, NumberFilter)

from lms.models.student import Student
from lms.models.absence import AbsenceType, AbsenceStatus, Absence


class AbsenceFilterSet(FilterSet):
    student = ModelChoiceFilter(field_name='student',
                                queryset=Student.objects.all())
    absence_type = ModelChoiceFilter(field_name='absence_type',
                                     queryset=AbsenceType.objects.all())
    absence_status = ModelChoiceFilter(field_name='absence_status',
                                       queryset=AbsenceStatus.objects.all())

    milgroup = NumberFilter(field_name='student__milgroup__milgroup')

    date_from = DateFilter(field_name='date', lookup_expr='gte')
    date_to = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Absence
        fields = ['milgroup']
