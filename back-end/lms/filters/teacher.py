from django_filters.rest_framework import FilterSet

from lms.models.teacher import Teacher


class TeacherFilter(FilterSet):

    class Meta:
        model = Teacher
        fields = ['milgroup', 'milgroup', 'milfaculty', 'rank', 'teacher_post']
