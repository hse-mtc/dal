from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from auth.models import Permission
from auth.permissions import BasePermission
from common.views.choices import GenericChoicesList
from lms.models.common import Milgroup
from lms.models.formations import FormationReport, FormationRemark
from lms.models.students import Student
from lms.models.teachers import Teacher
from lms.serializers.formations import (
    FormationReportSerializer,
    FormationRemarkSerializer,
)
from lms.utils.functions import get_personnel_from_request_user


class FormationReportPermission(BasePermission):
    permission_class = "formation-reports"
    view_name_rus = "Построения"
    methods = ["get", "post", "patch"]
    scopes = [Permission.Scope.MILFACULTY, Permission.Scope.MILGROUP]

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            personnel = get_personnel_from_request_user(request.user)
            if isinstance(personnel, Student) and (
                personnel.post == Student.Post.MILGROUP_COMMANDER
                and personnel.status == Student.Status.STUDYING
            ):
                return request.method.lower() in self.methods
        return super().has_permission(request, view)


class FormationRemarkPermission(BasePermission):
    permission_class = "formation-remarks"
    view_name_rus = "Замечания с построений"
    methods = ["get", "post", "patch", "delete"]
    scopes = [Permission.Scope.MILFACULTY]


def allowed_milgroup(user, milgroup, permission_class, method):
    if user.is_superuser:
        return True
    personnel = get_personnel_from_request_user(user)
    if isinstance(personnel, Student):
        return (
            permission_class == FormationReportPermission
            and personnel.post == Student.Post.MILGROUP_COMMANDER
            and personnel.status == Student.Status.STUDYING
            and personnel.milgroup_id == milgroup.id
        )
    if isinstance(personnel, Teacher):
        scope = user.get_perm_scope(permission_class.permission_class, method)
        if scope == Permission.Scope.ALL:
            return True
        if scope == Permission.Scope.MILFACULTY:
            return personnel.milfaculty_id == milgroup.milfaculty_id
        if (
            permission_class == FormationReportPermission
            and scope == Permission.Scope.MILGROUP
        ):
            return personnel.milgroups.filter(pk=milgroup.pk).exists()
        return False
    return False


class FormationReportViewSet(ModelViewSet):
    queryset = FormationReport.objects.select_related(
        "milgroup", "created_by", "updated_by"
    ).prefetch_related("remarks")
    serializer_class = FormationReportSerializer
    permission_classes = [FormationReportPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["date", "milgroup"]
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        personnel = get_personnel_from_request_user(self.request.user)
        if isinstance(personnel, Student) and (
            personnel.post == Student.Post.MILGROUP_COMMANDER
            and personnel.status == Student.Status.STUDYING
        ):
            return queryset.filter(milgroup=personnel.milgroup)
        if isinstance(personnel, Teacher):
            scope = self.request.user.get_perm_scope(
                FormationReportPermission.permission_class, self.request.method
            )
            if scope == Permission.Scope.ALL:
                return queryset
            if scope == Permission.Scope.MILFACULTY:
                return queryset.filter(milgroup__milfaculty=personnel.milfaculty)
            if scope == Permission.Scope.MILGROUP:
                return queryset.filter(milgroup__in=personnel.milgroups.all())
        return queryset.none()

    @action(detail=False, methods=["get"], url_path="roster-count")
    def roster_count(self, request):
        milgroup_id = request.query_params.get("milgroup")
        if not milgroup_id or not milgroup_id.isdecimal():
            raise ValidationError({"milgroup": "Укажите взвод"})
        milgroup = get_object_or_404(Milgroup, pk=milgroup_id)
        if not allowed_milgroup(
            request.user, milgroup, FormationReportPermission, "get"
        ):
            raise PermissionDenied()
        count = Student.objects.filter(
            milgroup=milgroup,
            status__in=[Student.Status.ENROLLED, Student.Status.STUDYING],
        ).count()
        return Response({"count": count})

    def perform_create(self, serializer):
        milgroup = serializer.validated_data["milgroup"]
        if not allowed_milgroup(
            self.request.user, milgroup, FormationReportPermission, "post"
        ):
            raise PermissionDenied()
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class FormationRemarkViewSet(ModelViewSet):
    queryset = FormationRemark.objects.select_related("report__milgroup", "student")
    serializer_class = FormationRemarkSerializer
    permission_classes = [FormationRemarkPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["report"]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        personnel = get_personnel_from_request_user(self.request.user)
        if isinstance(personnel, Teacher):
            scope = self.request.user.get_perm_scope(
                FormationRemarkPermission.permission_class, self.request.method
            )
            if scope == Permission.Scope.ALL:
                return queryset
            if scope == Permission.Scope.MILFACULTY:
                return queryset.filter(
                    report__milgroup__milfaculty=personnel.milfaculty
                )
        return queryset.none()

    def perform_create(self, serializer):
        report = serializer.validated_data["report"]
        if not allowed_milgroup(
            self.request.user, report.milgroup, FormationRemarkPermission, "post"
        ):
            raise PermissionDenied()
        serializer.save(created_by=self.request.user)


class FormationRemarkCategoryChoicesList(GenericChoicesList):
    choices_class = FormationRemark.Category
