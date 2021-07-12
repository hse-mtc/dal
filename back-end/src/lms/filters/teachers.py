from django_filters.rest_framework import FilterSet
from django_filters import NumberFilter

from lms.models.teachers import Teacher


class TeacherFilter(FilterSet):
    milgroup = NumberFilter(
        field_name="milgroups__id",
        lookup_expr="contains",
    )

    class Meta:
        model = Teacher
        fields = ["milgroup", "milfaculty", "rank", "post"]
