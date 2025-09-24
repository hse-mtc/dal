import typing as tp

from pathlib import Path

import requests

from django.db.models.query import QuerySet
from django.db.models import Subquery, OuterRef
from django.http import FileResponse

from rest_framework import status
from rest_framework import pagination

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import BaseRenderer

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema, OpenApiParameter


from common.models.universities import Campus
from conf import settings

from common.constants import MUTATE_ACTIONS

from common.models.milspecialties import Milspecialty

from auth.permissions import Permission, BasePermission

from ams.models.applicants import Applicant

from common.models.universities import Program

from ams.serializers.applicants import (
    ApplicantSerializer,
    ApplicantMutateSerializer,
    ApplicationProcessSerializer,
    ApplicantWithApplicationProcessSerializer,
)

from ams.filters.applicants import ApplicantFilter

from lms.models.students import Student
from lms.utils.mixins import QuerySetScopingMixin
from lms.types.personnel import Personnel
from ams.utils.export.default import generate_export as generate_def_export
from ams.utils.export.comp_sel_protocol import generate_export as generate_csp_export
from ams.utils.export.detailed import generate_applicants_detail
from ams.utils.export.enrolled_students import (
    generate_export as generate_enrolled_export,
)
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


class ApplicantDocsPermission(BasePermission):
    permission_class = "applicant_docs"
    view_name_rus = "Документы Абитуриента"
    methods = ["get"]
    scopes = [Permission.Scope.ALL]


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
            if hasattr(self.request.user, "applicant"):
                return self.queryset.filter(user__applicant=self.request.user.applicant)
            return self.queryset.none()

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

        if "marital_status" in request.data:
            display_to_code = {
                label: code for code, label in Applicant.MaritalStatus.choices
            }
            display_value = request.data["marital_status"]
            request.data["marital_status"] = display_to_code.get(
                display_value, Applicant.MaritalStatus.UNKNOWN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not self.milspecialty_is_selectable(
            request.data["milspecialty"], request.data["university_info"]["program"]
        ):
            return Response(
                {
                    "detail": "You can't select this milspecialty with your educational program"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
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

    def update(self, request, *args, **kwargs):
        applicant = Applicant.objects.get(pk=kwargs["pk"])
        request.data["user"] = applicant.user.id
        if (
            request.data["contact_info"]["corporate_email"]
            != applicant.contact_info.corporate_email
        ):
            return Response(
                {"detail": "Bad request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not self.milspecialty_is_selectable(
            request.data["milspecialty"], request.data["university_info"]["program"]
        ):
            return Response(
                {
                    "detail": "You can't select this milspecialty with your educational program"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        result = super(ApplicantViewSet, self).update(request, **kwargs)
        applicant.user.campuses = [request.data["university_info"]["campus"]]
        applicant.user.save()
        updated_applicant = Applicant.objects.get(pk=kwargs["pk"])
        generate_documents = request.data["generate_documents"]

        if generate_documents:
            generate_documents_for_applicant(updated_applicant)
        return result

    def milspecialty_is_selectable(self, milspecialty_id: int, program_id: int):
        milspecialty = Milspecialty.objects.filter(pk=milspecialty_id).first()
        return milspecialty.is_selectable_by_program(program_id)

    @transaction.atomic
    def perform_create(self, serializer):
        return serializer.save()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="campus", description="Filter by campus", required=True
            ),
            OpenApiParameter(name="program_code", description="Filter by program code"),
            OpenApiParameter(
                name="mtc_admission_year", description="Filter by admission year"
            ),
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

    def generate_students_excel_report(
        self,
        request: Request,
        excel_generator: tp.Callable[[QuerySet, QuerySet], Path],
    ) -> tp.Union[FileResponse, Response]:
        if (
            "campus" not in request.query_params
            or request.query_params["campus"] not in Campus
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        campus = request.query_params["campus"]
        year_param = request.query_params.get("mtc_admission_year")
        try:
            year = int(year_param) if year_param is not None else None
        except (TypeError, ValueError):
            year = None

        students = (
            Student.objects.filter(status=Student.Status.STUDYING)
            .select_related(
                "contact_info",
                "birth_info",
                "passport",
                "personal_documents_info",
                "university_info",
                "photo",
                "milgroup",
                "milgroup__milfaculty",
                "user",
                "university_info__program",
                "university_info__program__faculty",
            )
            .filter(university_info__program__faculty__campus=campus)
        )

        latest_app_year_sq = (
            Applicant.objects.filter(user=OuterRef("user"))
            .order_by("-application_process__mtc_admission_year", "-id")
            .values("application_process__mtc_admission_year")[:1]
        )
        students = students.annotate(mtc_admission_year=Subquery(latest_app_year_sq))

        if year is not None:
            students = students.filter(mtc_admission_year=year)

        students = students.order_by("surname", "name", "patronymic", "id")

        milspecialties = Milspecialty.objects.filter(available_for__contains=[campus])
        path = excel_generator(students, milspecialties)

        campus_name = dict(Campus.choices)[campus]
        return FileResponse(
            open(path, "rb"),
            as_attachment=True,
            filename=f"{campus_name}.xlsx",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    def generate_excel_report(
        self,
        request: Request,
        excel_generator: tp.Callable[[QuerySet, QuerySet], Path],
    ) -> tp.Union[FileResponse, Response]:
        if (
            "campus" not in request.query_params
            or request.query_params["campus"] not in Campus
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        students = self.get_queryset()

        if "mtc_admission_year" in request.query_params:
            mtc_admission_year = request.query_params["mtc_admission_year"]
            students = students.filter(
                application_process__mtc_admission_year=mtc_admission_year
            )

        campus = request.query_params["campus"]
        milspecialties = Milspecialty.objects.filter(available_for__contains=[campus])

        path = excel_generator(
            students.filter(university_info__program__faculty__campus=campus),
            milspecialties,
        )

        campus_name = dict(Campus.choices)[campus]
        response_file_name = f"{campus_name}.xlsx"

        file = open(path, "rb")
        return FileResponse(file, filename=response_file_name)

    def generate_docs(
        self,
    ) -> Response:
        applicants = self.get_queryset()
        data = [
            ApplicantSerializer(instance=applicant).data for applicant in applicants
        ]

        response = requests.get(
            f"http://{settings.WATCHDOC_HOST}:{settings.WATCHDOC_PORT}/generate_docs/",
            json=data,
        )

        if response.ok:
            return Response(
                response.content,
                headers={
                    "Content-Disposition": "attachment; filename=docs.zip",
                },
                content_type=response.headers.get("content-type"),
                status=response.status_code,
            )
        else:
            return Response(
                status=response.status_code,
            )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="campus", description="Filter by campus", required=True, type=str
            ),
            OpenApiParameter(
                name="mtc_admission_year", description="Filter by admission year"
            ),
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
            ),
            OpenApiParameter(
                name="mtc_admission_year", description="Filter by admission year"
            ),
        ]
    )
    @action(
        methods=["get"],
        url_path="students/export",
        detail=False,
        renderer_classes=[XLSXRenderer],
        permission_classes=[ApplicantPermission],
    )
    def students_export(self, request: Request) -> Response:
        """
        Send an excel file with info about ENROLLED students.
        Students are filtered by campus, specified in request query params.
        """
        return self.generate_students_excel_report(request, generate_enrolled_export)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="campus", description="Filter by campus", required=True, type=str
            ),
            OpenApiParameter(
                name="mtc_admission_year", description="Filter by admission year"
            ),
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="campus", description="Filter by campus", required=True, type=str
            ),
            OpenApiParameter(
                name="mtc_admission_year", description="Filter by admission year"
            ),
        ]
    )
    @action(
        methods=["get"],
        url_path="applications/applicants-detail/export",
        detail=False,
        renderer_classes=[XLSXRenderer],
        permission_classes=[ApplicantPermission],
    )
    def generate_applicants_detail_excel(self, request: Request) -> Response:
        return self.generate_excel_report(request, generate_applicants_detail)

    @action(
        methods=["get"],
        url_path="generate-docs",
        detail=False,
        renderer_classes=[XLSXRenderer],
        permission_classes=[ApplicantDocsPermission],
    )
    def applications_generate_docs(self, request: Request) -> Response:
        """
        Send an zip file with docs about applicants.
        Applicants are filtered by campus, specified in request query params.
        """
        return self.generate_docs()

    @extend_schema(request=None, responses={200: None})
    @action(
        detail=False,
        methods=["post"],
        url_path="resubmit-docs",
        permission_classes=[ApplicantPermission],
    )
    def resubmit_docs(self, request):
        """
        Resubmiting documents for the applicant.
        """
        applicant = Applicant.objects.filter(user=request.user).first()
        if not applicant:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        generate_documents_for_applicant(applicant)
        return Response(status=status.HTTP_200_OK)


def generate_documents_for_applicant(applicant: Applicant) -> None:
    data = ApplicantSerializer(instance=applicant).data
    response = requests.post(
        f"http://{settings.WATCHDOC_HOST}:{settings.WATCHDOC_PORT}/applicants/",
        json=data,
    )
    # TODO(TmLev): remove debug print
    print(response.json())
