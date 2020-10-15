import pytest


@pytest.mark.django_db
def test_trailing_slash_redirect(client):
    response = client.get("/api/dms/authors")
    assert response.status_code == 301

    response = client.get("/api/dms/authors/")
    assert response.status_code == 200
    assert not response.data
