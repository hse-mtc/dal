from django.db.models.query import QuerySet
from rest_framework import request
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema
from common.constants import MUTATE_ACTIONS

from lms.models.teachers import Teacher
from lms.models.students import Student
from lms.serializers.teachers import TeacherSerializer, TeacherMutateSerializer
from lms.filters.teachers import TeacherFilter

from auth.models import Permission
from auth.permissions import BasePermission


class TeacherPermission(BasePermission):
    permission_class = "teacher"


@extend_schema(tags=["teachers"])
class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()

    permission_classes = [TeacherPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = TeacherFilter
    search_fields = ["surname", "name", "patronymic"]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return TeacherMutateSerializer
        return TeacherSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset

        scope = self.request.user.get_perm_scope(
            TeacherPermission.permission_class, self.request.method)

        if scope >= Permission.Scopes.SELF:
            res = self.queryset.filter(user=self.request.user)
            if res.count() == 0:
                return QuerySet()
            return res

        if scope >= Permission.Scopes.MILFACULTY:
            milfaculty = None
            # check is user is a teacher
            user_teacher = self.queryset.filter(user=self.request.user)
            if user_teacher.count() == 0:
                # check if user is a student
                user_student = Student.objects.filter(user=self.request.user)
                if user_student.count() == 0:
                    # return nothing is user is not a student or a teacher
                    return QuerySet()
                # get student milfacuty
                milfaculty = user_student[0].milgroup.milfaculty
            else:
                # get teacher milfaculty
                milfaculty = user_teacher[0].milfaculty
            return self.queryset.filter(milfaculty=milfaculty)

        if scope >= Permission.Scopes.ALL:
            return self.queryset
 
        return QuerySet()
