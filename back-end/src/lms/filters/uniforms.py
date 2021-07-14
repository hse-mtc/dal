from django_filters.rest_framework import FilterSet

from lms.models.uniforms import Uniform


class UniformFilter(FilterSet):

    class Meta:
        model = Uniform
        fields = ["milfaculty"]
