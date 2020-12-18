from django_filters.rest_framework import (FilterSet, NumberFilter, DateFilter)

from lms.models.lesson import Lesson


class LessonFilter(FilterSet):
    milgroup = NumberFilter(field_name='milgroup__milgroup')

    date_from = DateFilter(field_name='date', lookup_expr='gte')
    date_to = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Lesson
        fields = ['ordinal']