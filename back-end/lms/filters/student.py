from django_filters.rest_framework import FilterSet, ModelChoiceFilter

from lms.models.common import Milgroup
from lms.models.student import Student


class StudentFilterSet(FilterSet):
    milgroup = ModelChoiceFilter(queryset=Milgroup.objects.all())

    class Meta:
        model = Student
        fields = ['status']
