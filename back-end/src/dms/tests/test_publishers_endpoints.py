import pytest
from dms.models.common import Publisher


def unpack_publisher(publisher: Publisher):
    return {
        "id": publisher.id,
        "name": publisher.name
    }


def create_publisher(name: str):
    publisher, _ = Publisher.objects.get_or_create(name=name)
    return publisher


@pytest.mark.django_db
def test_trailing_slash_redirect(su_client):
    wrong = su_client.get("/api/dms/publishers")
    assert wrong.status_code == 301

    right = su_client.get("/api/dms/publishers/")
    assert right.status_code == 200


@pytest.mark.django_db
def test_get_publishers_returns_list(su_client, publisher_data):
    pub_list = []
    for i in range(3):
        pub_data = publisher_data(name=f"Publisher {i}")
        publisher = create_publisher(**pub_data)
        pub_data = unpack_publisher(publisher)
        pub_list.append(pub_data)

    publishers_get_response = su_client.get("/api/dms/publishers/")
    assert publishers_get_response.status_code == 200

    publishers_get_response = publishers_get_response.json()
    for publisher in pub_list:
        assert publisher in publishers_get_response


@pytest.mark.django_db
def test_get_publishers_by_id(su_client, publisher_data):
    pub_data = publisher_data(name="Publisher with id")
    publisher = create_publisher(**pub_data)
    pub_data = unpack_publisher(publisher)

    publishers_get_response = su_client.get(f"/api/dms/publishers/{publisher.id}/")
    assert publishers_get_response.status_code == 200

    publishers_get_response = publishers_get_response.json()
    assert publishers_get_response == pub_data


@pytest.mark.django_db
def test_post_publishers_creates_publisher(su_client, publisher_data):
    first = su_client.post(
        "/api/dms/publishers/",
        publisher_data(),
        content_type="application/json"
    )
    assert first.status_code == 201

    second = su_client.post("/api/dms/publishers/", publisher_data())
    assert second.status_code == 201

    assert first.data["id"] != second.data["id"]


@pytest.mark.django_db
def test_put_changes_name(su_client, publisher_data):
    id_ = create_publisher(**publisher_data(name="Testing put method")).id

    changes = {"name": "Changed name"}
    put_response = su_client.put(
        f"/api/dms/publishers/{id_}/",
        changes,
        content_type="application/json"
    )
    assert put_response.status_code == 200
    publisher = Publisher.objects.get(id=id_)
    assert publisher.name == changes["name"]


@pytest.mark.django_db
def test_delete_deletes_publisher(su_client, publisher_data):
    pub_data = publisher_data(name="Publisher Name")
    publisher, _ = Publisher.objects.get_or_create(**pub_data)
    pub_data = unpack_publisher(publisher)

    delete_response = su_client.delete(f"/api/dms/publishers/{publisher.id}/")
    assert delete_response.status_code == 204
    exists = True
    try:
        Publisher.objects.get(id=pub_data["id"])
    except Publisher.DoesNotExist:
        exists = False
    assert not exists


@pytest.mark.django_db
def test_patch_formats_publisher(su_client, publisher_data):
    id_ = create_publisher(**publisher_data(name="Testing put method")).id

    changes = {"name": "New name"}
    put_response = su_client.patch(
        f"/api/dms/publishers/{id_}/",
        changes,
        content_type="application/json"
    )
    assert put_response.status_code == 200
    publisher = Publisher.objects.get(id=id_)
    assert publisher.name == changes["name"]
