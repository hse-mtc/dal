from django_filters.rest_framework import (FilterSet, NumberFilter)

from lms.models.mark import Mark


class MarkFilter(FilterSet):
    milgroup = NumberFilter(field_name='student__milgroup__milgroup')

    class Meta:
        model = Mark
        fields = ['student', 'lesson']
