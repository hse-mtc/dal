from django_filters.rest_framework import (FilterSet, DateFilter)

from lms.models.achievement import Achievement


class AchievementFilter(FilterSet):

    date_from = DateFilter(field_name='date', lookup_expr='gte')
    date_to = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Achievement
        fields = ['student', 'achievement_type']
