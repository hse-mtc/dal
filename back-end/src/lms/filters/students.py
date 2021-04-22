from django_filters.rest_framework import (FilterSet, CharFilter)

from lms.models.students import Student


class StudentFilter(FilterSet):

    phone = CharFilter(field_name='contact_info__personal_phone_number')

    class Meta:
        model = Student
        fields = ['status', 'milgroup']
