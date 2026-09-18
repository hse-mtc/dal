# pylint: disable=redefined-outer-name,invalid-name
import base64
from unittest.mock import patch

import pytest

from auth.models import Permission
from common.models.personal import Photo


@pytest.fixture
def su_client_mo(su_client, superuser):
    superuser.campuses = ["MO"]
    superuser.save()
    return su_client


@pytest.mark.django_db
def test_registration_data_does_not_read_photo(su_client_mo, applicant):
    applicant.photo = Photo.objects.create(image="photos/unavailable.jpg")
    applicant.save()
    url = f"/api/ams/applicants/{applicant.pk}/"

    with patch(
        "ams.serializers.applicants.ApplicantSerializer.get_photo",
        return_value="large-photo",
    ):
        full_data = su_client_mo.get(url).json()

    with patch.object(
        applicant.photo.image.storage,
        "open",
        side_effect=AssertionError("Registration must not open the photo"),
    ) as open_photo:
        response = su_client_mo.get(url, {"for_student": "true"})

    assert response.status_code == 200
    open_photo.assert_not_called()
    assert response.json() == {
        key: value for key, value in full_data.items() if key not in {"photo", "family"}
    }
    assert response.json()["user"] == applicant.user_id
    assert response.json()["university_info"]["program"]["id"] == (
        applicant.university_info.program_id
    )


@pytest.mark.django_db
@pytest.mark.parametrize("params", [{}, {"for_student": "false"}])
def test_regular_retrieve_keeps_photo_and_family(su_client_mo, applicant, params):
    applicant.photo = Photo.objects.create(image="photos/existing.jpg")
    applicant.save()

    with patch.object(applicant.photo.image.storage, "open") as open_photo:
        open_photo.return_value.read.return_value = b"photo-content"
        response = su_client_mo.get(f"/api/ams/applicants/{applicant.pk}/", params)

    assert response.status_code == 200
    assert response.json()["photo"] == base64.b64encode(b"photo-content").decode()
    assert "family" in response.json()
    open_photo.assert_called_once()


@pytest.mark.django_db
def test_registration_data_requires_permission(test_client, applicant):
    response = test_client.get(
        f"/api/ams/applicants/{applicant.pk}/", {"for_student": "true"}
    )
    assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize("is_owner,expected_status", [(True, 200), (False, 404)])
def test_registration_data_respects_self_scope(
    test_client, test_user, applicant, is_owner, expected_status
):
    test_user.campuses = ["MO"]
    test_user.permissions.add(
        Permission.objects.create(
            viewset="applicants", method="get", scope=Permission.Scope.SELF
        )
    )
    test_user.save()
    if is_owner:
        applicant.user = test_user
        applicant.save()

    response = test_client.get(
        f"/api/ams/applicants/{applicant.pk}/", {"for_student": "true"}
    )
    assert response.status_code == expected_status
