from django_filters.rest_framework import (FilterSet, ModelChoiceFilter,
                                           DateFilter, NumberFilter)

from lms.models.student import Student
from lms.models.teacher import Teacher
from lms.models.encouragement import EncouragementType, Encouragement


class EncouragementFilterSet(FilterSet):
    student = ModelChoiceFilter(field_name='student',
                                queryset=Student.objects.all())
    teacher = ModelChoiceFilter(field_name='teacher',
                                queryset=Teacher.objects.all())
    encouragement_type = ModelChoiceFilter(
        field_name='encouragement_type',
        queryset=EncouragementType.objects.all())

    milgroup = NumberFilter(field_name='student__milgroup__milgroup')

    date_from = DateFilter(field_name='date', lookup_expr='gte')
    date_to = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Encouragement
        fields = ['reason', 'milgroup']
