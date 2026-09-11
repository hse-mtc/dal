import pytest

from django.contrib import admin
from django.db import connection
from django.test import RequestFactory
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from ams.models.applicants import Applicant, ApplicationProcess


pytestmark = pytest.mark.django_db


def get_request(superuser, path, params=None):
    request = RequestFactory().get(path, params or {})
    request.user = superuser
    return request


def render_change_view(superuser, applicant):
    model_admin = admin.site._registry[Applicant]
    path = reverse("admin:ams_applicant_change", args=[applicant.pk])
    response = model_admin.change_view(get_request(superuser, path), str(applicant.pk))
    response.render()


def test_applicant_admin_searches_by_name_email_and_id(superuser, applicant):
    model_admin = admin.site._registry[Applicant]
    path = reverse("admin:ams_applicant_changelist")

    for search_term in [
        "Тестов Тест",
        applicant.contact_info.corporate_email,
        str(applicant.pk),
    ]:
        response = model_admin.changelist_view(
            get_request(superuser, path, {"q": search_term})
        )
        assert list(response.context_data["cl"].result_list) == [applicant]


def test_applicant_admin_filters_by_year_and_campus(superuser, applicant):
    applicant.application_process.mtc_admission_year = 2026
    applicant.application_process.save(update_fields=["mtc_admission_year"])

    model_admin = admin.site._registry[Applicant]
    path = reverse("admin:ams_applicant_changelist")
    response = model_admin.changelist_view(
        get_request(
            superuser,
            path,
            {
                "application_process__mtc_admission_year__exact": "2026",
                "university_info__program__faculty__campus__exact": "MO",
            },
        )
    )

    assert list(response.context_data["cl"].result_list) == [applicant]


def test_application_process_admin_searches_by_applicant_name(superuser, applicant):
    model_admin = admin.site._registry[ApplicationProcess]
    path = reverse("admin:ams_applicationprocess_changelist")
    queryset, may_have_duplicates = model_admin.get_search_results(
        get_request(superuser, path), ApplicationProcess.objects.all(), "Тестов Тест"
    )

    assert list(queryset) == [applicant.application_process]
    assert may_have_duplicates is False


def test_applicant_change_queries_do_not_scale_with_application_processes(
    superuser, applicant
):
    render_change_view(superuser, applicant)
    with CaptureQueriesContext(connection) as baseline_queries:
        render_change_view(superuser, applicant)

    ApplicationProcess.objects.bulk_create([ApplicationProcess() for _ in range(30)])
    with CaptureQueriesContext(connection) as scaled_queries:
        render_change_view(superuser, applicant)

    assert len(scaled_queries) <= len(baseline_queries) + 1


def test_application_process_list_does_not_query_applicants_per_row(
    superuser, applicant
):
    ApplicationProcess.objects.bulk_create([ApplicationProcess() for _ in range(30)])
    model_admin = admin.site._registry[ApplicationProcess]
    path = reverse("admin:ams_applicationprocess_changelist")

    with CaptureQueriesContext(connection) as queries:
        response = model_admin.changelist_view(get_request(superuser, path))
        response.render()

    standalone_applicant_queries = [
        query["sql"] for query in queries if 'FROM "ams_applicant"' in query["sql"]
    ]
    assert standalone_applicant_queries == []
