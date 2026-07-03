# pylint: disable=redefined-outer-name,invalid-name
"""Тесты лёгкого переноса абитуриента между ВУС.

Инвариант: эндпоинт меняет только `Applicant.milspecialty`, проверяет
совместимость с образовательной программой и кампусом, и НЕ трогает
`ApplicationProcess` (физо/оценки) и документы.
"""
import pytest

from common.models.milspecialties import Milspecialty

MILSPECIALTY_URL = "/api/ams/applicants/{pk}/milspecialty/"


@pytest.fixture
def su_client_mo(su_client, superuser):
    """su_client, которому виден кампус MO (иначе filter_queryset отсечёт запись)."""
    superuser.campuses = ["MO"]
    superuser.save()
    return su_client


@pytest.mark.django_db
def test_move_to_compatible_milspecialty(su_client_mo, applicant):
    """Совместимый ВУС (доступен для кампуса, выбираем любой программой) -> 200."""
    target = Milspecialty.objects.create(
        title="Новый ВУС", code="453000", available_for=["MO"]
    )
    ap_before = applicant.application_process

    resp = su_client_mo.patch(
        MILSPECIALTY_URL.format(pk=applicant.id),
        {"milspecialty": target.id},
        content_type="application/json",
    )
    assert resp.status_code == 200
    assert resp.json()["code"] == "453000"

    applicant.refresh_from_db()
    assert applicant.milspecialty_id == target.id

    # ApplicationProcess не тронут
    ap_before.refresh_from_db()
    assert ap_before.physical_test_grade == 0
    assert ap_before.mean_grade == 0


@pytest.mark.django_db
def test_move_to_milspecialty_not_selectable_by_program(su_client_mo, applicant):
    """ВУС, недопустимый для программы абитуриента -> 400, ВУС не меняется."""
    original_id = applicant.milspecialty_id
    target = Milspecialty.objects.create(
        title="Ограниченный ВУС",
        code="106646-543",
        available_for=["MO"],
        selectable_by_every_program=False,
    )

    resp = su_client_mo.patch(
        MILSPECIALTY_URL.format(pk=applicant.id),
        {"milspecialty": target.id},
        content_type="application/json",
    )
    assert resp.status_code == 400

    applicant.refresh_from_db()
    assert applicant.milspecialty_id == original_id


@pytest.mark.django_db
def test_move_to_milspecialty_not_available_for_campus(su_client_mo, applicant):
    """ВУС, недоступный для кампуса абитуриента (MO) -> 400."""
    original_id = applicant.milspecialty_id
    target = Milspecialty.objects.create(
        title="Питерский ВУС", code="999999", available_for=["SP"]
    )

    resp = su_client_mo.patch(
        MILSPECIALTY_URL.format(pk=applicant.id),
        {"milspecialty": target.id},
        content_type="application/json",
    )
    assert resp.status_code == 400

    applicant.refresh_from_db()
    assert applicant.milspecialty_id == original_id


@pytest.mark.django_db
def test_move_forbidden_without_permission(test_client, applicant):
    target = Milspecialty.objects.create(
        title="Новый ВУС", code="453000", available_for=["MO"]
    )
    resp = test_client.patch(
        MILSPECIALTY_URL.format(pk=applicant.id),
        {"milspecialty": target.id},
        content_type="application/json",
    )
    assert resp.status_code == 403
