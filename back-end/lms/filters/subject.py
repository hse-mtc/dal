from django_filters.rest_framework import FilterSet

from common.models.subjects import Subject


class SubjectFilter(FilterSet):

    class Meta:
        model = Subject
        fields = [
            'title',
        ]
