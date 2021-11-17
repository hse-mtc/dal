# pylint: disable=redefined-outer-name
import json
import os

from uuid import UUID

import pytest

from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.core.files.base import ContentFile

from PIL import Image, ImageChops

from dms.models.documents import File
from dms.models.books import Cover, Book

from auth.models import Permission


def dump_data(data):
    json_data = data.copy()
    json_data["data"] = json.dumps(json_data["data"])
    return json_data


def send_create_request(client, data):
    create_response = client.post("/api/dms/books/", data=dump_data(data))
    assert create_response.status_code == 201
    return create_response


def assert_images_equal(image_1_path: str, image_2_path: str):
    with Image.open(image_1_path) as img1, Image.open(image_2_path) as img2:
        # Convert to same mode and size for comparison
        img2 = img2.convert(img1.mode)
        img2 = img2.resize(img1.size)

        diff = ImageChops.difference(img1, img2)

        assert not diff.getbbox()


def assert_book_data_equal(su_client, original_data, book_id):
    get_response = su_client.get(f"/api/dms/books/{book_id}/")
    assert get_response.status_code == 200

    response_data = get_response.data
    file = File.objects.get(id=response_data["file"]["content"].rsplit(
        "/", maxsplit=1)[-1].rsplit("_", maxsplit=1)[0])
    to_compare_fields = [
        "title", "annotation", "upload_date", "publication_year", "page_count",
        "authors", "publishers", "subjects"
    ]

    image = ""
    if isinstance(response_data["cover"], UUID):
        image = Cover.objects.get(id=response_data["cover"])
    else:
        img_id = response_data["cover"]["image"].rsplit(
            "/", maxsplit=1)[-1].split("_")[0]
        image = Cover.objects.get(id=img_id)
    assert_images_equal(original_data["image"], image.image)
    assert file.content.open("r").read() == original_data["content"].open(
        "r").read()
    assert {
        field_name: response_data[field_name]
        for field_name in to_compare_fields
    } == {
        field_name: original_data["data"][field_name]
        for field_name in to_compare_fields
    }


@pytest.fixture(autouse=True)
def remove_permissions(test_user):
    yield
    test_user.permissions.clear()


def give_permission_to_user(user, data):
    permission = Permission.objects.create(**data)
    user.permissions.add(permission)
    user.save()


@pytest.mark.django_db
# pylint: disable=too-many-arguments
def test_post_books_creates_new_book(su_client, book_data, author_data,
                                     publisher_data, subject_data):
    data = book_data(author_data, publisher_data, subject_data)
    create_response = send_create_request(su_client, data)

    book_id = create_response.data["id"]
    assert_book_data_equal(su_client, data, book_id)


@pytest.mark.django_db
# pylint: disable=too-many-arguments
def test_put_update_book(su_client, book_data, author_data, publisher_data,
                         subject_data):
    data = book_data(author_data, publisher_data, subject_data)
    create_response = send_create_request(su_client, data)

    book_id = create_response.data["id"]
    data = book_data(author_data,
                     publisher_data,
                     subject_data,
                     title="new_title",
                     annotation="new_annotation")
    json_data = data.copy()
    json_data["data"] = json.dumps(data["data"])
    content = encode_multipart(
        boundary=BOUNDARY,
        data=json_data,
    )
    update_response = su_client.put(f"/api/dms/books/{book_id}/",
                                    data=content,
                                    content_type=MULTIPART_CONTENT)
    assert update_response.status_code == 200
    assert_book_data_equal(su_client, data, book_id)


@pytest.mark.django_db
# pylint: disable=too-many-arguments
def test_patch_update_book(su_client, book_data, author_data, publisher_data,
                           subject_data):
    data = book_data(author_data, publisher_data, subject_data)
    create_response = send_create_request(su_client, data)

    book_id = create_response.data["id"]
    file = ContentFile("file_content_new", name="file.txt")
    data["content"] = file
    content = encode_multipart(
        boundary=BOUNDARY,
        data={
            "content": file,
            "data": json.dumps({"title": "new_title_2"})
        },
    )
    update_response = su_client.patch(f"/api/dms/books/{book_id}/",
                                      data=content,
                                      content_type=MULTIPART_CONTENT)
    assert update_response.status_code == 200
    data["data"]["title"] = "new_title_2"
    assert_book_data_equal(su_client, data, book_id)


@pytest.mark.django_db
# pylint: disable=too-many-arguments
def test_delete_book(su_client, book_data, author_data, publisher_data,
                     subject_data):
    data = book_data(author_data, publisher_data, subject_data)
    create_response = send_create_request(su_client, data)

    book_id = create_response.data["id"]
    delete_response = su_client.delete(f"/api/dms/books/{book_id}/")
    assert delete_response.status_code == 204
    get_response = su_client.get(f"/api/dms/books/{book_id}/")
    assert get_response.status_code == 404


@pytest.mark.django_db
def test_invalid_cover(su_client, book_data, author_data, publisher_data,
                       subject_data):
    data = book_data(author_data, publisher_data, subject_data)
    data["image"] = ContentFile("file_content", name="file_name.png")
    create_response = su_client.post("/api/dms/books/", data=dump_data(data))
    assert create_response.status_code == 400
    assert "image" in create_response.json()

    data = book_data(author_data, publisher_data, subject_data)
    create_response = send_create_request(su_client, data)
    book_id = create_response.data["id"]
    json_data = data.copy()
    json_data["image"] = "test_str"
    json_data["data"] = json.dumps(data["data"])
    content = encode_multipart(
        boundary=BOUNDARY,
        data=json_data,
    )
    update_response = su_client.put(f"/api/dms/books/{book_id}/",
                                    data=content,
                                    content_type=MULTIPART_CONTENT)
    assert update_response.status_code == 400
    assert "image" in update_response.json()

    content = encode_multipart(
        boundary=BOUNDARY,
        data={"image": ContentFile("file_content", name="file_name.png")},
    )
    update_response = su_client.patch(f"/api/dms/books/{book_id}/",
                                      data=content,
                                      content_type=MULTIPART_CONTENT)
    assert update_response.status_code == 400
    assert "image" in update_response.json()


@pytest.mark.django_db
def test_only_content(su_client):
    create_response = su_client.post(
        "/api/dms/books/",
        data={"content": ContentFile("file_content_new", name="file.txt")})
    assert create_response.status_code == 201

    book_id = create_response.data["id"]
    get_response = su_client.get(f"/api/dms/books/{book_id}/")
    assert get_response.status_code == 200

    create_response = su_client.post("/api/dms/books/",
                                     data={"content": "string"})
    assert create_response.status_code == 400
    assert "content" in create_response.json()


@pytest.mark.django_db
def test_post_create_with_null_data(su_client):
    create_response = su_client.post("/api/dms/books/", data=None)
    assert create_response.status_code == 400


@pytest.mark.django_db
def test_get_book_with_permissions(test_client, test_user, permission_data):
    get_response = test_client.get(f"/api/dms/books/{-1}/")
    assert get_response.status_code == 403
    give_permission_to_user(test_user, permission_data("books", "get", "all"))
    get_response = test_client.get(f"/api/dms/books/{-1}/")
    assert get_response.status_code == 404


# pylint: disable=too-many-arguments
def send_create_request_with_permissions(test_client, test_user,
                                         permission_data, book_data,
                                         author_data, publisher_data,
                                         subject_data,
                                         post_create_permission_scope):
    give_permission_to_user(test_user, permission_data("books", "get", "all"))
    give_permission_to_user(
        test_user, permission_data("books", "post",
                                   post_create_permission_scope))
    data = book_data(author_data, publisher_data, subject_data)
    data["data"]["user"] = test_user.id
    create_response = send_create_request(test_client, data)

    book_id = create_response.data["id"]
    get_response = test_client.get(f"/api/dms/books/{book_id}/")
    assert get_response.status_code == 200

    test_user.permissions.clear()


@pytest.mark.django_db
# pylint: disable=too-many-arguments
def test_post_books_with_permissions(test_client, test_user, permission_data,
                                     book_data, author_data, publisher_data,
                                     subject_data):
    send_create_request_with_permissions(test_client, test_user,
                                         permission_data, book_data,
                                         author_data, publisher_data,
                                         subject_data, "self")

    test_user.permissions.clear()

    send_create_request_with_permissions(test_client, test_user,
                                         permission_data, book_data,
                                         author_data, publisher_data,
                                         subject_data, "all")


@pytest.mark.django_db
# pylint: disable=too-many-arguments
def test_patch_books_with_permissions(test_client, test_user, permission_data,
                                      book_data, author_data, publisher_data,
                                      subject_data):
    give_permission_to_user(test_user, permission_data("books", "get", "all"))
    give_permission_to_user(test_user, permission_data("books", "post", "self"))
    give_permission_to_user(test_user, permission_data("books", "patch",
                                                       "self"))
    data = book_data(author_data, publisher_data, subject_data)
    data["data"]["user"] = test_user.id
    create_response = send_create_request(test_client, data)

    book_id = create_response.data["id"]
    file = ContentFile("file_content_new", name="file.txt")
    data["content"] = file
    data["data"]["user"] = test_user.id
    content = encode_multipart(
        boundary=BOUNDARY,
        data={
            "content": file,
            "data": json.dumps({"title": "new_title_2"})
        },
    )
    update_response = test_client.patch(f"/api/dms/books/{book_id}/",
                                        data=content,
                                        content_type=MULTIPART_CONTENT)
    assert update_response.status_code == 200


@pytest.mark.django_db
# pylint: disable=too-many-arguments
def test_patch_books_without_permissions(su_client, test_client, test_user,
                                         permission_data, book_data,
                                         author_data, publisher_data,
                                         subject_data):
    give_permission_to_user(test_user, permission_data("books", "get", "all"))
    data = book_data(author_data, publisher_data, subject_data)
    data["data"]["user"] = test_user.id
    create_response = send_create_request(su_client, data)

    book_id = create_response.data["id"]
    file = ContentFile("file_content_new", name="file.txt")
    data["content"] = file
    data["data"]["user"] = test_user.id
    content = encode_multipart(
        boundary=BOUNDARY,
        data={
            "content": file,
            "data": json.dumps({"title": "new_title_2"})
        },
    )
    update_response = test_client.patch(f"/api/dms/books/{book_id}/",
                                        data=content,
                                        content_type=MULTIPART_CONTENT)
    assert update_response.status_code == 403

    give_permission_to_user(test_user, permission_data("books", "patch", "all"))
    update_response = test_client.patch(f"/api/dms/books/{book_id}/",
                                        data=content,
                                        content_type=MULTIPART_CONTENT)
    assert update_response.status_code == 200


@pytest.mark.django_db
# pylint: disable=too-many-arguments
def test_delete_books_with_permissions(su_client, test_client, test_user,
                                       permission_data, book_data, author_data,
                                       publisher_data, subject_data):
    data = book_data(author_data, publisher_data, subject_data)
    data["data"]["user"] = test_user.id
    create_response = send_create_request(su_client, data)

    book_id = create_response.data["id"]
    delete_response = test_client.delete(f"/api/dms/books/{book_id}/")
    assert delete_response.status_code == 403
    give_permission_to_user(test_user, permission_data("books", "delete",
                                                       "all"))
    delete_response = test_client.delete(f"/api/dms/books/{book_id}/")
    assert delete_response.status_code == 204

    test_user.permissions.clear()
    give_permission_to_user(test_user, permission_data("books", "post", "self"))
    data = book_data(author_data, publisher_data, subject_data)
    data["data"]["user"] = test_user.id
    create_response = send_create_request(test_client, data)

    book_id = create_response.data["id"]
    delete_response = test_client.delete(f"/api/dms/books/{book_id}/")
    assert delete_response.status_code == 403
    give_permission_to_user(test_user, permission_data("books", "delete",
                                                       "self"))
    delete_response = test_client.delete(f"/api/dms/books/{book_id}/")
    assert delete_response.status_code == 204


@pytest.mark.django_db
# pylint: disable=too-many-arguments
def test_delete_book_deletes_cover_and_file(su_client, book_data, author_data,
                                            publisher_data, subject_data):
    data = book_data(author_data, publisher_data, subject_data)
    create_response = send_create_request(su_client, data)

    book = Book.objects.get(pk=create_response.json()["id"])
    cover_id = book.cover.pk
    file_id = book.file.pk

    image_path = f"/back-end/media/covers/{create_response.data['cover']}"
    assert os.path.isfile(image_path)

    file_path = f"/back-end/{create_response.data['file']['content']}"
    assert os.path.isfile(file_path)

    assert Cover.objects.filter(pk=cover_id).exists()
    assert File.objects.filter(pk=file_id).exists()

    book_id = create_response.data["id"]
    su_client.delete(f"/api/dms/books/{book_id}/")

    assert not Cover.objects.filter(pk=cover_id).exists()
    assert not File.objects.filter(pk=file_id).exists()
    assert not os.path.isfile(image_path)
    assert not os.path.isfile(file_path)


@pytest.mark.django_db
# pylint: disable=too-many-arguments
def test_change_book_deletes_old_cover_and_file(su_client, book_data,
                                                author_data, publisher_data,
                                                subject_data, image):
    data = book_data(author_data, publisher_data, subject_data)
    create_response = send_create_request(su_client, data)

    book_id = create_response.json()["id"]
    book = Book.objects.get(pk=book_id)
    cover_id = book.cover.pk
    file_id = book.file.pk

    image_path_before = \
        f"/back-end/media/covers/{create_response.data['cover']}"
    assert os.path.isfile(image_path_before)
    with open(image_path_before, "rb") as f:
        old_image_content = f.read()

    file_path_before = f"/back-end/{create_response.data['file']['content']}"
    assert os.path.isfile(file_path_before)
    with open(file_path_before, "rb") as f:
        old_file_content = f.read()
    assert Cover.objects.filter(pk=cover_id).exists()
    assert File.objects.filter(pk=file_id).exists()

    file = ContentFile("file_content_new", name="file_new.txt")
    image_file = image("image_new.png", color=(255, 0, 0))
    content = encode_multipart(
        boundary=BOUNDARY,
        data={
            "content": file,
            "image": image_file,
        },
    )
    update_response = su_client.patch(f"/api/dms/books/{book_id}/",
                                      data=content,
                                      content_type=MULTIPART_CONTENT)
    assert update_response.status_code == 200

    file_path_after = f"/back-end/{update_response.data['file']['content']}"
    image_path_after = f"/back-end/media/covers/{update_response.data['cover']}"
    assert image_path_before == image_path_after

    with open(image_path_after, "rb") as f:
        new_image_content = f.read()
        assert old_image_content != new_image_content

    assert file_path_before == file_path_after

    with open(image_path_after, "rb") as f:
        new_file_content = f.read()
        assert old_file_content != new_file_content
