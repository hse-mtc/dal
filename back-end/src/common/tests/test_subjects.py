import pytest
from common.models.subjects import Subject


def unpack_subject(subject: Subject):
    return {
        "id": subject.id,
        "title": subject.title,
        "annotation": subject.annotation,
        "milspecialty": subject.milspecialty.id,
    }


@pytest.mark.django_db
def test_trailing_slash_redirect(su_client):
    wrong = su_client.get("/api/lms/subjects")
    assert wrong.status_code == 301

    right = su_client.get("/api/lms/subjects/")
    assert right.status_code == 200


@pytest.mark.django_db
def test_get_subject_by_id(
    su_client, create_milspecialty, get_new_subject_data, create_subject
):
    milspecialty = create_milspecialty(
        title="Математическое обеспечения комплексов ПРО", code="453100"
    )
    subj_data = get_new_subject_data(
        title="Строевая подготовка", milspecialty=milspecialty
    )
    subject = create_subject(**subj_data)
    subj_data = unpack_subject(subject)
    subject_get_response = su_client.get(f"/api/lms/subjects/{subject.id}/")
    assert subject_get_response.status_code == 200

    subject_get_response = subject_get_response.json()
    assert subject_get_response == subj_data


@pytest.mark.django_db
def test_get_subjects_by_title(
    su_client, create_milspecialty, get_new_subject_data, create_subject
):
    milspecialty = create_milspecialty(
        title="Математическое обеспечения комплексов ПРО", code="453100"
    )
    subj_data = get_new_subject_data(
        title="Тактическая подготовка", milspecialty=milspecialty
    )
    subject = create_subject(**subj_data)
    subj_data = unpack_subject(subject)

    subject_response_get = su_client.get(f"/api/lms/subjects/?title={subject.title}")
    assert subject_response_get.status_code == 200

    subject_response_get = subject_response_get.json()
    assert len(subject_response_get) >= 1
    for subject in subject_response_get:
        subj_data["id"] = subject["id"]
        assert subject == subj_data


@pytest.mark.django_db
def test_get_subjects_by_search(
    su_client, create_milspecialty, get_new_subject_data, create_subject
):
    milspecialty = create_milspecialty(
        title="Математическое обеспечения комплексов ПРО", code="453100"
    )
    subj_data = get_new_subject_data(
        title="Тактико-специальная подготовка 2", milspecialty=milspecialty
    )
    subject = create_subject(**subj_data)
    word = subject.title.split()[1]

    subject_response_get = su_client.get(f"/api/lms/subjects/?search={word}")
    assert subject_response_get.status_code == 200

    subject_response_get = subject_response_get.json()
    assert len(subject_response_get) >= 1
    for subject in subject_response_get:
        assert subject["title"].find(word) != -1
