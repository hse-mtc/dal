import typing as tp

from pathlib import Path

import requests

from django.db.models.query import QuerySet

from rest_framework import status
from rest_framework import pagination

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import BaseRenderer

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema, OpenApiParameter

from conf import settings

from common.constants import MUTATE_ACTIONS

from common.models.milspecialties import Milspecialty

from auth.permissions import Permission, BasePermission

from ams.models.applicants import Applicant

from ams.serializers.applicants import (
    ApplicantSerializer,
    ApplicantMutateSerializer,
    ApplicationProcessSerializer,
    ApplicantWithApplicationProcessSerializer,
)

from ams.filters.applicants import ApplicantFilter

from lms.utils.mixins import QuerySetScopingMixin
from lms.types.personnel import Personnel
from ams.utils.export.default import generate_export as generate_def_export
from ams.utils.export.comp_sel_protocol import generate_export as generate_csp_export
from django.db import transaction

class XLSXRenderer(BaseRenderer):
    media_type = "application/xlsx"
    format = "xlsx"
    charset = None
    render_style = "binary"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class ApplicantPermission(BasePermission):
    permission_class = "applicants"
    view_name_rus = "Абитуриенты"
    methods = ["get", "post", "patch", "put"]
    scopes = [Permission.Scope.ALL, Permission.Scope.SELF]


class ApplicantPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"


@extend_schema(tags=["applicants"])
class ApplicantViewSet(QuerySetScopingMixin, ModelViewSet):
    # pylint: disable=too-many-public-methods
    queryset = Applicant.objects.order_by("surname", "name", "patronymic", "id")

    permission_classes = [ApplicantPermission]
    scoped_permission_class = ApplicantPermission

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = ApplicantFilter
    search_fields = ["surname", "name", "patronymic"]

    pagination_class = ApplicantPageNumberPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method
        )
        if scope == Permission.Scope.ALL:
            return self.queryset.all()

        if scope == Permission.Scope.SELF and (
            self.action == "partial_update"
            or self.action == "retrieve"
            or self.action == "update"
        ):
            return self.queryset.filter(user__applicant=self.request.user.applicant)

        return self.queryset.none()

    def is_creation_allowed_by_scope(
        self,
        data: dict,
    ) -> bool:
        if self.request.user.is_superuser:
            return True

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method
        )

        if scope == Permission.Scope.ALL or scope == Permission.Scope.SELF:
            return True

        return False

    def get_serializer_class(self):
        if self.action == "applications":
            return ApplicantWithApplicationProcessSerializer
        if self.action == "application":
            return ApplicationProcessSerializer
        if self.action in MUTATE_ACTIONS:
            return ApplicantMutateSerializer
        return ApplicantSerializer

    def filter_queryset(self, queryset):
        campuses = self.request.user.campuses
        qs = super().filter_queryset(queryset)
        return qs.filter(university_info__program__faculty__campus__in=campuses)

    def create(self, request, *args, **kwargs):
        # pylint: disable=too-many-locals

        request.data["user"] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.campuses = [self.request.data["university_info"]["campus"]]
        self.request.user.save()
        if self.is_creation_allowed_by_scope(request.data):
            generate_documents = serializer.validated_data.pop("generate_documents")
            applicant = self.perform_create(serializer)

            if generate_documents:
                generate_documents_for_applicant(applicant)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=self.get_success_headers(serializer.data),
            )
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    def update(self, request, **kwargs):
        request.data["user"] = Applicant.objects.get(pk=kwargs["pk"]).user.id
        return super(ApplicantViewSet, self).update(request, **kwargs)

    @transaction.atomic
    def perform_create(self, serializer):
        return serializer.save()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="campus", description="Filter by campus", required=True
            ),
            OpenApiParameter(name="program_code", description="Filter by program code"),
        ]
    )
    @action(detail=False, methods=["get"], permission_classes=[ApplicantPermission])
    def applications(self, request: Request, *args, **kwargs) -> Response:
        """List all applicants with their applications."""
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=["patch"], permission_classes=[ApplicantPermission])
    def application(self, request: Request, pk=None) -> Response:
        """Create or edit applicant's application."""

        # pylint: disable=unused-argument,invalid-name
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        applicant = self.get_object()

        updated = serializer.update(
            instance=applicant.application_process,
            validated_data=serializer.validated_data,
        )
        applicant.application_process = updated
        applicant.save()

        return Response(
            status=status.HTTP_200_OK,
            data=ApplicationProcessSerializer(instance=updated).data,
        )

    def generate_excel_report(
        self,
        request: Request,
        excel_generator: tp.Callable[[QuerySet, QuerySet], Path],
    ) -> Response:
        if "campus" not in request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        students = self.get_queryset()

        campus = request.query_params["campus"]
        milspecialties = Milspecialty.objects.filter(available_for__contains=[campus])

        path = excel_generator(students, milspecialties)
        with open(path, "rb") as file:
            export = file.read()
        path.unlink(missing_ok=True)

        return Response(
            export,
            headers={
                "Content-Disposition": "attachment; filename=export.xlsx",
            },
            content_type="application/xlsx",
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="campus", description="Filter by campus", required=True, type=str
            )
        ]
    )
    @action(
        methods=["get"],
        url_path="applications/export",
        detail=False,
        renderer_classes=[XLSXRenderer],
        permission_classes=[ApplicantPermission],
    )
    def applications_export(self, request: Request) -> Response:
        """
        Send an excel file with info about applicants.
        Applicants are filtered by campus, specified in request query params.
        """
        return self.generate_excel_report(request, generate_def_export)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="campus", description="Filter by campus", required=True, type=str
            )
        ]
    )
    @action(
        methods=["get"],
        url_path="applications/competitive-selection-protocol/export",
        detail=False,
        renderer_classes=[XLSXRenderer],
        permission_classes=[ApplicantPermission],
    )
    def generate_comp_sel_protocol(self, request: Request) -> Response:
        """
        Send an excel protocol file with info about applicants.
        Applicants are filtered by campus, specified in request query params.
        File includes a header from a template.
        """
        return self.generate_excel_report(request, generate_csp_export)


def generate_documents_for_applicant(applicant: Applicant) -> None:
    data = ApplicantSerializer(instance=applicant).data
    response = requests.post(
        f"http://{settings.WATCHDOC_HOST}:{settings.WATCHDOC_PORT}/applicants/",
        data=JSONRenderer().render(data),
    )
    # TODO(TmLev): remove debug print
    print(response.json())
