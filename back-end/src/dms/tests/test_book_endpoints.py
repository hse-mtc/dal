# pylint: disable=redefined-outer-name
import pytest

from PIL import Image

import numpy as np

from dms.models.documents import File
from dms.models.books import Cover


def assert_images_equal(image_1_path: str, image_2_path):
    with Image.open(image_1_path) as img1, Image.open(image_2_path) as img2:
        # Convert to same mode and size for comparison
        img2 = img2.convert(img1.mode)
        img2 = img2.resize(img1.size)

        sum_sq_diff = np.sum((np.asarray(img1).astype("float") -
                              np.asarray(img2).astype("float"))**2)

        if sum_sq_diff == 0:
            # Images are exactly the same
            pass
        else:
            normalized_sum_sq_diff = sum_sq_diff / np.sqrt(sum_sq_diff)
            assert normalized_sum_sq_diff < 0.001


@pytest.mark.django_db
# pylint: disable=too-many-arguments
def test_post_books_creates_new_book(su_client, book_data, cover_data,
                                     author_data, publisher_data, subject_data):
    data = book_data(cover_data, author_data, publisher_data, subject_data)
    create_response = su_client.post("/api/dms/books/", data)
    assert create_response.status_code == 201

    book_id = create_response.data["id"]
    get_response = su_client.get(f"/api/dms/books/{book_id}/")
    assert get_response.status_code == 200

    print(get_response.json())
    data["favorite"] = False
    file = File.objects.get(
        id=get_response.data["file"]["content"].rsplit("/", maxsplit=1)[-1])
    print(get_response.data["file"]["content"].rsplit("/", maxsplit=1)[-1])
    to_compare_fields = [
        "favorite", "title", "annotation", "upload_date", "publication_year",
        "page_count", "authors", "publishers", "subjects"
    ]
    image = Cover.objects.get(
        id=get_response.data["cover"]["image"].rsplit("/", maxsplit=1)[-1])
    assert_images_equal(data["image"], image.image)
    assert file.content.open("r").read() == data["content"].open("r").read()
    assert {
        field_name: get_response.data[field_name]
        for field_name in to_compare_fields
    } == {field_name: data[field_name] for field_name in to_compare_fields}
