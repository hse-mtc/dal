from django.db.models.query import QuerySet
import requests

from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer
from drf_spectacular.views import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from lms.models.uniforms import Uniform
from lms.models.teachers import Teacher
from lms.models.students import Student
from lms.serializers.uniforms import UniformSerializer, UniformMutateSerializer
from lms.filters.uniforms import UniformFilter

from conf.settings import (
    TGBOT_PORT,
    TGBOT_HOST,
)
from common.constants import MUTATE_ACTIONS
from auth.permissions import BasePermission, register_view_permissions


class UniformPermission(BasePermission):
    permission_class = 'uniform'

register_view_permissions('uniform', 'Форма одежды', scopes=['all', 'milfaculty'])


@extend_schema(tags=['uniforms'])
class UniformViewSet(ModelViewSet):
    queryset = Uniform.objects.all()

    permission_classes = [UniformPermission]
    filter_backends = [DjangoFilterBackend]

    filterset_class = UniformFilter

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return UniformMutateSerializer
        return UniformSerializer

    def perform_update(self, serializer: UniformSerializer):
        serializer.save()
        requests.post(
            f'http://{TGBOT_HOST}:{TGBOT_PORT}/uniforms/',
            data=JSONRenderer().render(serializer.data),
        )
    
    # pylint: disable=too-many-return-statements
    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        
        scope = self.request.user.get_perm_scope(
            UniformPermission.permission_class, self.request.method)
        
        if scope == Permission.Scopes.MILFACULTY:
            milfaculty = None
            # check is user is a teacher
            user_teacher = Teacher.objects.filter(user=self.request.user)
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

        is scope == Permission.Scopes.ALL:
            return self.queryset

        return QuerySet()
