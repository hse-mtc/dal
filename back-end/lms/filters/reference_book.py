from django_filters.rest_framework import FilterSet

from lms.models.common import Milgroup
from lms.models.student import Program


class MilgroupFilter(FilterSet):

    class Meta:
        model = Milgroup
        fields = '__all__'


class ProgramFilter(FilterSet):

    class Meta:
        model = Program
        fields = '__all__'
