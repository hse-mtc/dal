from django_filters.rest_framework import FilterSet

from common.models.subjects import Subject


class LessonSubjectFilter(FilterSet):

    class Meta:
        model = Subject
        fields = ["title"]
