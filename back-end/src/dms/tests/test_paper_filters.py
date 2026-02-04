# pylint: disable=redefined-outer-name
import pytest


@pytest.fixture
def create_paper_with_extra_fields(
    su_client, paper_data, non_string_paper_data, format_multipart_for_post_request
):
    """Helper to create papers with additional_fields"""

    def call_me(additional_fields=None, **kwargs):
        data = paper_data(**kwargs)
        non_string_data = non_string_paper_data()
        data["data"] |= non_string_data

        if additional_fields:
            data["data"]["additional_fields"] = additional_fields

        response = su_client.post(
            "/api/dms/papers/", format_multipart_for_post_request(data)
        )
        assert response.status_code == 201
        return response.data["id"]

    return call_me


@pytest.mark.django_db
def test_filter_json_eq_operator(su_client, create_paper_with_extra_fields):
    """Test eq operator for exact match with number"""
    # Create papers with different values
    create_paper_with_extra_fields(
        additional_fields={"число тут": 10, "другое поле": "значение"}, title="Paper 1"
    )
    create_paper_with_extra_fields(
        additional_fields={"число тут": 20, "другое поле": "значение"}, title="Paper 2"
    )
    create_paper_with_extra_fields(
        additional_fields={"число тут": 10, "другое поле": "другое"}, title="Paper 3"
    )

    # Test eq filter
    response = su_client.get("/api/dms/papers/", {"extra_filter": "eq|число тут|10"})
    assert response.status_code == 200
    assert len(response.data) == 2
    titles = [paper["title"] for paper in response.data]
    assert "Paper 1" in titles
    assert "Paper 3" in titles
    assert "Paper 2" not in titles


@pytest.mark.django_db
def test_filter_json_contains_operator(su_client, create_paper_with_extra_fields):
    """Test contains operator for substring match"""
    create_paper_with_extra_fields(
        additional_fields={"фильтр вот такой": "лт"}, title="Paper with лт"
    )
    create_paper_with_extra_fields(
        additional_fields={"фильтр вот такой": "другое значение лт здесь"},
        title="Paper with лт inside",
    )
    create_paper_with_extra_fields(
        additional_fields={"фильтр вот такой": "без этого"}, title="Paper without"
    )

    # Test contains filter
    response = su_client.get(
        "/api/dms/papers/", {"extra_filter": "contains|фильтр вот такой|лт"}
    )
    assert response.status_code == 200
    assert len(response.data) == 2
    titles = [paper["title"] for paper in response.data]
    assert "Paper with лт" in titles
    assert "Paper with лт inside" in titles
    assert "Paper without" not in titles


@pytest.mark.django_db
def test_filter_json_and_combination(su_client, create_paper_with_extra_fields):
    """Test AND combination of multiple filters - this is the bug case"""
    # Create papers with various combinations
    create_paper_with_extra_fields(
        additional_fields={"число тут": 10, "фильтр вот такой": "лт"},
        title="Paper matches both",
    )
    create_paper_with_extra_fields(
        additional_fields={"число тут": 10, "фильтр вот такой": "не то"},
        title="Paper matches only number",
    )
    create_paper_with_extra_fields(
        additional_fields={"число тут": 20, "фильтр вот такой": "лт"},
        title="Paper matches only text",
    )
    create_paper_with_extra_fields(
        additional_fields={"число тут": 20, "фильтр вот такой": "не то"},
        title="Paper matches neither",
    )

    # Test AND combination
    response = su_client.get(
        "/api/dms/papers/",
        {"extra_filter": ["eq|число тут|10", "contains|фильтр вот такой|лт"]},
    )
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Paper matches both"


@pytest.mark.django_db
def test_filter_json_in_operator(su_client, create_paper_with_extra_fields):
    """Test in operator for multiple values"""
    create_paper_with_extra_fields(
        additional_fields={"статус": "активен"}, title="Active paper"
    )
    create_paper_with_extra_fields(
        additional_fields={"статус": "архив"}, title="Archive paper"
    )
    create_paper_with_extra_fields(
        additional_fields={"статус": "удален"}, title="Deleted paper"
    )

    # Test in filter with multiple values
    response = su_client.get(
        "/api/dms/papers/", {"extra_filter": "in|статус|активен,архив"}
    )
    assert response.status_code == 200
    assert len(response.data) == 2
    titles = [paper["title"] for paper in response.data]
    assert "Active paper" in titles
    assert "Archive paper" in titles
    assert "Deleted paper" not in titles


@pytest.mark.django_db
def test_filter_json_lte_operator(su_client, create_paper_with_extra_fields):
    """Test lte operator for less than or equal"""
    create_paper_with_extra_fields(additional_fields={"балл": 5}, title="Paper with 5")
    create_paper_with_extra_fields(
        additional_fields={"балл": 10}, title="Paper with 10"
    )
    create_paper_with_extra_fields(
        additional_fields={"балл": 15}, title="Paper with 15"
    )

    # Test lte filter
    response = su_client.get("/api/dms/papers/", {"extra_filter": "lte|балл|10"})
    assert response.status_code == 200
    assert len(response.data) == 2
    titles = [paper["title"] for paper in response.data]
    assert "Paper with 5" in titles
    assert "Paper with 10" in titles
    assert "Paper with 15" not in titles


@pytest.mark.django_db
def test_filter_json_gte_operator(su_client, create_paper_with_extra_fields):
    """Test gte operator for greater than or equal"""
    create_paper_with_extra_fields(additional_fields={"балл": 5}, title="Paper with 5")
    create_paper_with_extra_fields(
        additional_fields={"балл": 10}, title="Paper with 10"
    )
    create_paper_with_extra_fields(
        additional_fields={"балл": 15}, title="Paper with 15"
    )

    # Test gte filter
    response = su_client.get("/api/dms/papers/", {"extra_filter": "gte|балл|10"})
    assert response.status_code == 200
    assert len(response.data) == 2
    titles = [paper["title"] for paper in response.data]
    assert "Paper with 10" in titles
    assert "Paper with 15" in titles
    assert "Paper with 5" not in titles


@pytest.mark.django_db
def test_filter_json_and_with_numeric_comparisons(
    su_client, create_paper_with_extra_fields
):
    """Test AND combination with numeric comparison operators"""
    create_paper_with_extra_fields(
        additional_fields={"мин балл": 5, "макс балл": 15}, title="Paper 5-15"
    )
    create_paper_with_extra_fields(
        additional_fields={"мин балл": 8, "макс балл": 12}, title="Paper 8-12"
    )
    create_paper_with_extra_fields(
        additional_fields={"мин балл": 11, "макс балл": 20}, title="Paper 11-20"
    )

    # Test range filter: мин балл >= 7 AND макс балл <= 13
    response = su_client.get(
        "/api/dms/papers/", {"extra_filter": ["gte|мин балл|7", "lte|макс балл|13"]}
    )
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Paper 8-12"


@pytest.mark.django_db
def test_filter_json_complex_and_combination(su_client, create_paper_with_extra_fields):
    """Test complex AND combination with different operator types"""
    create_paper_with_extra_fields(
        additional_fields={
            "число тут": 10,
            "фильтр вот такой": "лт",
            "статус": "активен",
        },
        title="Full match",
    )
    create_paper_with_extra_fields(
        additional_fields={
            "число тут": 10,
            "фильтр вот такой": "лт",
            "статус": "архив",
        },
        title="Partial match 1",
    )
    create_paper_with_extra_fields(
        additional_fields={
            "число тут": 20,
            "фильтр вот такой": "лт",
            "статус": "активен",
        },
        title="Partial match 2",
    )

    # Test 3-way AND
    response = su_client.get(
        "/api/dms/papers/",
        {
            "extra_filter": [
                "eq|число тут|10",
                "contains|фильтр вот такой|лт",
                "eq|статус|активен",
            ]
        },
    )
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Full match"


@pytest.mark.django_db
def test_filter_json_empty_results(su_client, create_paper_with_extra_fields):
    """Test that filters return empty when no matches"""
    create_paper_with_extra_fields(additional_fields={"число тут": 10}, title="Paper 1")

    # Test filter that shouldn't match
    response = su_client.get("/api/dms/papers/", {"extra_filter": "eq|число тут|999"})
    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_filter_json_with_string_numbers(su_client, create_paper_with_extra_fields):
    """Test eq operator handles both numeric and string values"""
    # Numbers can be stored as strings in JSON
    create_paper_with_extra_fields(
        additional_fields={"число": "10"}, title="String number"
    )
    create_paper_with_extra_fields(
        additional_fields={"число": 10}, title="Numeric number"
    )

    # Should match both string and numeric representation
    response = su_client.get("/api/dms/papers/", {"extra_filter": "eq|число|10"})
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_filter_json_and_combination_comma_separated(
    su_client, create_paper_with_extra_fields
):
    """
    Test AND combination when filters are passed as comma-separated string.

    This is the bug case:
    - User sends: ?extra_filter=eq|число тут|10,contains|фильтр вот такой|лт
    - Expected: AND combination of both filters
    - Actual: Fails because the string is not properly parsed

    The filter should handle both:
    1. ?extra_filter=eq|..&extra_filter=contains|.. (array)
    2. ?extra_filter=eq|..,contains|.. (comma-separated string)
    """
    # Create papers with various combinations
    create_paper_with_extra_fields(
        additional_fields={"число_тут": 10, "фильтр_такой": "лт"},
        title="Paper matches both",
    )
    create_paper_with_extra_fields(
        additional_fields={"число_тут": 10, "фильтр_такой": "не то"},
        title="Paper matches only number",
    )
    create_paper_with_extra_fields(
        additional_fields={"число_тут": 20, "фильтр_такой": "лт"},
        title="Paper matches only text",
    )

    # Test with comma-separated string (the bug case)
    # This simulates: ?extra_filter=eq|число_тут|10,contains|фильтр_такой|лт
    response = su_client.get(
        "/api/dms/papers/",
        {"extra_filter": "eq|число_тут|10,contains|фильтр_такой|лт"},
    )
    assert response.status_code == 200
    # BUG: Currently this returns 0 results because the filter doesn't parse
    # comma-separated tokens correctly
    # After fix, should return 1 result ("Paper matches both")
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Paper matches both"
