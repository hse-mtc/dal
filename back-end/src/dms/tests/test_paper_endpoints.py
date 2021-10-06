# pylint: disable=redefined-outer-name
import random

import pytest
from django.test.client import MULTIPART_CONTENT

from dms.models.papers import Category, Paper
from dms.models.documents import File
from dms.models.common import Author, Publisher


@pytest.fixture
def non_string_paper_data(author_data, publisher_data, category_data):

    def call_me(num_authors: int = 1, num_publishers: int = 1):

        return {
            "authors": [
                Author.objects.create(**author_data()).id
                for _ in range(num_authors)
            ],
            "publishers": [
                Publisher.objects.create(**publisher_data()).id
                for _ in range(num_publishers)
            ],
            "category": Category.objects.create(**category_data()).id
        }

    return call_me


@pytest.mark.django_db
def test_trailing_slash_redirect(su_client):
    response = su_client.get("/api/dms/papers")
    assert response.status_code == 301

    response = su_client.get("/api/dms/papers/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_papers_creates_new_paper(su_client, paper_data,
                                       non_string_paper_data,
                                       format_multipart_for_post_request):
    data = paper_data()
    data["data"] |= non_string_paper_data()
    res = format_multipart_for_post_request(data)
    response = su_client.post("/api/dms/papers/", res)
    assert response.status_code == 201
    id_ = response.data["id"]

    response = su_client.get(f"/api/dms/papers/{id_}/")
    assert response.status_code == 200

    file = File.objects.get(
        id=response.data["file"]["content"].rsplit("/", maxsplit=1)[-1])
    to_compare_fields = [
        "title", "annotation", "upload_date", "publication_date", "is_binned",
        "category", "authors", "publishers"
    ]
    assert file.content.open("r").read() == data["content"].open("r").read()
    assert {
        field_name: response.data[field_name]
        for field_name in to_compare_fields
    } == {
        field_name: data["data"][field_name] for field_name in to_compare_fields
    }


@pytest.mark.django_db
def test_get_searches_papers_by_title_and_annotation(
        su_client, paper_data, non_string_paper_data,
        format_multipart_for_post_request):
    data = paper_data(title="Танки Великой Отечественной войны", annotation="")
    non_string_data = non_string_paper_data()
    data |= non_string_data
    response = su_client.post("/api/dms/papers/",
                              format_multipart_for_post_request(data))
    assert response.status_code == 201

    for _ in range(5):
        data = paper_data(title=random.choice(
            ["Тактика боя", "Устав", "Справочник офицера"]),
                          annotation="")
        data |= non_string_data
        response = su_client.post("/api/dms/papers/",
                                  format_multipart_for_post_request(data))
        assert response.status_code == 201

    response = su_client.get("/api/dms/papers/", {"search": "танк"})
    assert response.status_code == 200
    assert len(response.data) == 1

    data = paper_data(title="Танки США и NATO",
                      annotation="Каталог танков США и НАТО")
    data |= non_string_data
    response = su_client.post("/api/dms/papers/",
                              format_multipart_for_post_request(data))
    assert response.status_code == 201

    response = su_client.get("/api/dms/papers/", {"search": "танк"})
    assert response.status_code == 200
    assert len(response.data) == 2

    response = su_client.get("/api/dms/papers/",
                             {"search": "Каталог танков США"})
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_get_searches_by_id(su_client, paper_data, non_string_paper_data,
                            format_multipart_for_post_request):
    title = "Танки Великой Отечественной войны"
    data = paper_data(title=title)
    non_string_data = non_string_paper_data()
    data |= non_string_data
    response = su_client.post("/api/dms/papers/",
                              format_multipart_for_post_request(data))
    assert response.status_code == 201

    id_ = response.data["id"]
    response = su_client.get(f"/api/dms/papers/{id_}/")
    assert response.status_code == 200
    assert response.data["id"] == id_
    assert response.data["title"] == title


@pytest.mark.django_db
def test_put_uploads_new_paper_content(su_client, paper_data,
                                       non_string_paper_data,
                                       format_multipart_for_put_request,
                                       format_multipart_for_post_request):
    content = b"File content"
    data = paper_data(file_content=content)
    non_string_data = non_string_paper_data()
    data["data"] |= non_string_data

    response = su_client.post("/api/dms/papers/",
                              data=format_multipart_for_post_request(data),
                              content_type=MULTIPART_CONTENT)
    assert response.status_code == 201

    id_ = response.data["id"]
    paper1 = Paper.objects.get(id=id_)
    assert paper1.file.content.open("rb").read() == content

    content2 = b"File content 2"
    data = paper_data(file_content=content2)
    data["data"] |= non_string_data

    response = su_client.put(path=f"/api/dms/papers/{id_}/",
                             data=format_multipart_for_put_request(data),
                             content_type=MULTIPART_CONTENT)
    assert response.status_code == 200

    id_ = response.data["id"]
    paper1 = Paper.objects.get(id=id_)
    assert paper1.file.content.open("rb").read() == content2


@pytest.mark.django_db
def test_patch_edits_book(su_client, paper_data, non_string_paper_data,
                          format_multipart_for_post_request):
    title = "title_1"
    data = paper_data(title=title)
    non_string_data = non_string_paper_data()
    data |= non_string_data
    response = su_client.post("/api/dms/papers/",
                              format_multipart_for_post_request(data))
    assert response.status_code == 201

    id_ = response.data["id"]
    paper = Paper.objects.get(id=id_)
    assert paper.title == title
    title2 = "title_2"
    response = su_client.patch(f"/api/dms/papers/{id_}/", {"title": title2},
                               content_type="application/json")
    assert response.status_code == 200

    paper = Paper.objects.get(id=id_)
    assert paper.title == title2


@pytest.mark.django_db
def test_delete_removes_book(su_client, paper_data, non_string_paper_data,
                             format_multipart_for_post_request):
    annotation = "annotation 3"
    data = paper_data(annotation=annotation)
    non_string_data = non_string_paper_data()
    data |= non_string_data
    response = su_client.post("/api/dms/papers/",
                              format_multipart_for_post_request(data))
    assert response.status_code == 201
    assert len(Paper.objects.filter(annotation=annotation)) == 1

    id_ = response.data["id"]
    response = su_client.delete(f"/api/dms/papers/{id_}/")
    assert response.status_code == 204
    assert len(Paper.objects.filter(annotation=annotation)) == 0
