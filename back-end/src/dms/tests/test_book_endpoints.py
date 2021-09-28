# pylint: disable=redefined-outer-name
import pytest

@pytest.mark.django_db
def test_post_books_creates_new_book(su_client, book_data, cover_data, author_data, publisher_data, subject_data):
    create_request = su_client.post("/api/dms/books/", book_data(cover_data, author_data, publisher_data, subject_data))
    print(create_request.json())
    assert create_request.status_code == 201
    book_id = create_request.data["id"]
