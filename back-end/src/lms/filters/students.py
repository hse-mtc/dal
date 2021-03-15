from django_filters.rest_framework import FilterSet

from lms.models.students import Student


class StudentFilter(FilterSet):

    class Meta:
        model = Student
        fields = ['status', 'milgroup']
