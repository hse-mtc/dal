from django_filters.rest_framework import FilterSet

from common.models.universities import Program


class ProgramFilter(FilterSet):

    class Meta:
        model = Program
        fields = "__all__"
