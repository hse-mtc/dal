from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions

from django.contrib.auth import get_user_model

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema
from common.constants import MUTATE_ACTIONS

from lms.models.teachers import Teacher
from lms.serializers.teachers import TeacherSerializer, TeacherMutateSerializer
from lms.filters.teachers import TeacherFilter
from lms.mixins import QuerySetScopingMixin

from auth.models import Permission
from auth.permissions import BasePermission


class TeacherPermission(BasePermission):
    permission_class = "teachers"
    view_name_rus = "Преподаватель"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
        Permission.Scope.SELF,
    ]


@extend_schema(tags=["teachers"])
class TeacherViewSet(QuerySetScopingMixin, ModelViewSet):
    queryset = Teacher.objects.all()

    permission_classes = [TeacherPermission]
    scoped_permission_class = TeacherPermission

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = TeacherFilter
    search_fields = ["surname", "name", "patronymic"]

    def get_serializer_class(self):
        mutate_actions = MUTATE_ACTIONS + ["registration"]
        if self.action in mutate_actions:
            return TeacherMutateSerializer
        return TeacherSerializer

    @action(detail=False,
            methods=["post"],
            permission_classes=[permissions.AllowAny])
    def registration(self, request):
        # TODO(TmLev): verify email uniqueness. Create Teacher model.

        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data["email"]
        user = get_user_model().objects.create_user(
            email=email,
            password=get_user_model().objects.make_random_password(),
        )

        serializer.save()
        teacher = Teacher.objects.get(id=serializer.data.id)
        teacher.user = user
        teacher.save()
        return Response(TeacherSerializer(data=teacher).data)

    def handle_scope_milfaculty(self, user_type, user):
        if user_type == "student":
            milfaculty = user.milgroup.milfaculty
        elif user_type == "teacher":
            milfaculty = user.milfaculty
        else:
            return self.queryset.none()
        return self.queryset.filter(milfaculty=milfaculty)

    def allow_scope_milfaculty_on_create(self, data, user_type, user):
        if user_type == "student":
            milfaculty = user.milgroup.milfaculty
        elif user_type == "teacher":
            milfaculty = user.milfaculty
        else:
            return False
        return data["milfaculty"] == milfaculty.id

    def handle_scope_self(self, user_type, user):
        if user_type == "teacher":
            return self.queryset.filter(user=self.request.user)
        return self.queryset.none()

    def allow_scope_self_on_create(self, data, user_type, user):
        if user_type == "teacher":
            return data["user"] == user.id
        return False
