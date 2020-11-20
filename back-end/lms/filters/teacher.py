from django_filters.rest_framework import FilterSet, ModelChoiceFilter

from lms.models.common import Milgroup, Milfaculty
from lms.models.teacher import Rank, TeacherPost, Teacher


class TeacherFilterSet(FilterSet):
    milgroup = ModelChoiceFilter(queryset=Milgroup.objects.all())
    milfaculty = ModelChoiceFilter(queryset=Milfaculty.objects.all())
    rank = ModelChoiceFilter(queryset=Rank.objects.all())
    teacher_post = ModelChoiceFilter(queryset=TeacherPost.objects.all())

    class Meta:
        model = Teacher
        fields = ['milgroup']
