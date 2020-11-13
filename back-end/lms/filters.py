from django_filters.rest_framework import (FilterSet, ModelChoiceFilter,
                                           DateFilter, NumberFilter)

from lms.models import (Student, Milgroup, Milfaculty, Absence, AbsenceType,
                        AbsenceStatus, Teacher, Rank, TeacherPost, Punishment,
                        PunishmentType)


class StudentFilterSet(FilterSet):
    milgroup = ModelChoiceFilter(queryset=Milgroup.objects.all())

    class Meta:
        model = Student
        fields = ['status']


class AbsenceFilterSet(FilterSet):
    student = ModelChoiceFilter(field_name='student',
                                queryset=Student.objects.all())
    absence_type = ModelChoiceFilter(field_name='absence_type',
                                     queryset=AbsenceType.objects.all())
    absence_status = ModelChoiceFilter(field_name='absence_status',
                                       queryset=AbsenceStatus.objects.all())

    milgroup = NumberFilter(field_name='student__milgroup__milgroup')

    date_from = DateFilter(field_name='date', lookup_expr='gte')
    date_to = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Absence
        fields = ['milgroup']


class TeacherFilterSet(FilterSet):
    milgroup = ModelChoiceFilter(queryset=Milgroup.objects.all())
    milfaculty = ModelChoiceFilter(queryset=Milfaculty.objects.all())
    rank = ModelChoiceFilter(queryset=Rank.objects.all())
    teacher_post = ModelChoiceFilter(queryset=TeacherPost.objects.all())

    class Meta:
        model = Teacher
        fields = ['milgroup']


class PunishmentFilterSet(FilterSet):
    student = ModelChoiceFilter(field_name='student',
                                queryset=Student.objects.all())
    teacher = ModelChoiceFilter(field_name='teacher',
                                queryset=Teacher.objects.all())
    punishment_type = ModelChoiceFilter(field_name='punishment_type',
                                        queryset=PunishmentType.objects.all())

    milgroup = NumberFilter(field_name='student__milgroup__milgroup')

    date_from = DateFilter(field_name='date', lookup_expr='gte')
    date_to = DateFilter(field_name='date', lookup_expr='lte')

    remove_date_from = DateFilter(field_name='remove_date', lookup_expr='gte')
    remove_date_to = DateFilter(field_name='remove_date', lookup_expr='lte')

    class Meta:
        model = Punishment
        fields = ['reason', 'milgroup']
