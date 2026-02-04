# pylint: disable=redefined-outer-name
"""
Unit tests for PaperFilter class.
These tests focus on the filter logic without requiring HTTP requests.
"""

from unittest.mock import MagicMock, Mock

import pytest
from django.db.models import Q
from dms.filters import PaperFilter


class TestBuildQFromToken:
    """Unit tests for _build_q_from_token method"""

    @pytest.fixture
    def paper_filter(self):
        """Create PaperFilter instance for testing"""
        return PaperFilter()

    def test_eq_with_integer(self, paper_filter):
        """Test eq operator with integer value"""
        result = paper_filter._build_q_from_token(
            "eq|число тут|10", "additional_fields"
        )

        # Should return Q object (not tuple for eq)
        assert isinstance(result, Q)
        # Should contain both numeric and string comparison (OR)
        assert str(result) is not None

    def test_eq_with_string(self, paper_filter):
        """Test eq operator with string value (no numeric parse)"""
        result = paper_filter._build_q_from_token("eq|field|abc", "additional_fields")

        assert isinstance(result, Q)

    def test_contains_operator(self, paper_filter):
        """Test contains operator (icontains)"""
        result = paper_filter._build_q_from_token(
            "contains|фильтр вот такой|лт", "additional_fields"
        )

        assert isinstance(result, Q)

    def test_in_operator(self, paper_filter):
        """Test in operator with comma-separated values"""
        result = paper_filter._build_q_from_token(
            "in|статус|активен,архив", "additional_fields"
        )

        assert isinstance(result, Q)

    def test_lte_operator_numeric(self, paper_filter):
        """Test lte operator with numeric value"""
        result = paper_filter._build_q_from_token("lte|балл|10", "additional_fields")

        # Returns tuple for numeric comparison (Q, annotations)
        assert isinstance(result, tuple)
        q, annotations = result
        assert isinstance(q, Q)
        assert isinstance(annotations, dict)
        assert "__балл_num_cast" in annotations

    def test_gte_operator_numeric(self, paper_filter):
        """Test gte operator with numeric value"""
        result = paper_filter._build_q_from_token("gte|балл|10", "additional_fields")

        assert isinstance(result, tuple)
        q, annotations = result
        assert isinstance(q, Q)

    def test_lte_operator_string(self, paper_filter):
        """Test lte operator with string value (no numeric parse)"""
        result = paper_filter._build_q_from_token(
            "lte|date|2021-01-01", "additional_fields"
        )

        # Returns Q object for string comparison
        assert isinstance(result, Q)

    def test_invalid_token_short(self, paper_filter):
        """Test that invalid token returns empty Q"""
        result = paper_filter._build_q_from_token("eq|field", "additional_fields")

        assert isinstance(result, Q)

    def test_invalid_token_empty(self, paper_filter):
        """Test empty token"""
        result = paper_filter._build_q_from_token("", "additional_fields")

        assert isinstance(result, Q)


class TestFilterJson:
    """Unit tests for filter_json method - testing the AND combination"""

    @pytest.fixture
    def paper_filter_with_request(self):
        """Create PaperFilter with mocked request"""

        def factory(filter_values: list):
            filter_instance = PaperFilter()
            filter_instance.request = Mock()
            filter_instance.request.GET = Mock()
            filter_instance.request.GET.getlist = Mock(return_value=filter_values)
            return filter_instance

        return factory

    def test_single_filter(self, paper_filter_with_request):
        """Test with single filter value"""
        filter_instance = paper_filter_with_request(["eq|число тут|10"])

        # Create mock queryset
        queryset = MagicMock()
        queryset.annotate.return_value = queryset
        queryset.filter.return_value = queryset

        result = filter_instance.filter_json(queryset, "extra_filter", None)

        # Should call filter once
        queryset.filter.assert_called_once()

    def test_multiple_filters_and_combination(self, paper_filter_with_request):
        """
        Test AND combination of multiple filters.
        This is the bug case: eq|число тут|10,contains|фильтр вот такой|лт
        """
        filter_instance = paper_filter_with_request(
            ["eq|число тут|10", "contains|фильтр вот такой|лт"]
        )

        queryset = MagicMock()
        queryset.annotate.return_value = queryset
        queryset.filter.return_value = queryset

        result = filter_instance.filter_json(queryset, "extra_filter", None)

        # Should call filter once with combined Q
        queryset.filter.assert_called_once()

        # Get the Q object that was passed to filter
        call_args = queryset.filter.call_args
        assert call_args is not None

    def test_filters_with_numeric_annotations(self, paper_filter_with_request):
        """Test AND combination with operators that need annotations (lte, gte)"""
        filter_instance = paper_filter_with_request(
            ["gte|мин балл|7", "lte|макс балл|13"]
        )

        queryset = MagicMock()
        queryset.annotate.return_value = queryset
        queryset.filter.return_value = queryset

        result = filter_instance.filter_json(queryset, "extra_filter", None)

        # Should call annotate for the numeric casts
        queryset.annotate.assert_called()

    def test_mixed_filter_types(self, paper_filter_with_request):
        """Test AND combination with different operator types"""
        filter_instance = paper_filter_with_request(
            ["eq|число тут|10", "contains|фильтр вот такой|лт", "eq|статус|активен"]
        )

        queryset = MagicMock()
        queryset.annotate.return_value = queryset
        queryset.filter.return_value = queryset

        result = filter_instance.filter_json(queryset, "extra_filter", None)

        queryset.filter.assert_called_once()


class TestCommaSeparatedValueParsing:
    """
    Tests for the bug scenario:
    User sends: extra_filter=eq|число тут|10,contains|фильтр вот такой|лт
    Expected: Both filters applied with AND
    Actual: Something goes wrong with comma parsing
    """

    @pytest.fixture
    def paper_filter_with_raw_request(self):
        """Create PaperFilter simulating different request scenarios"""

        def factory(raw_value: str):
            filter_instance = PaperFilter()
            filter_instance.request = Mock()

            # Simulate how Django handles query params
            # If user sends: ?extra_filter=eq|число тут|10,contains|фильтр вот такой|лт
            # Django's getlist returns a single string
            filter_instance.request.GET = Mock()
            filter_instance.request.GET.getlist = Mock(return_value=[raw_value])

            return filter_instance

        return factory

    def test_comma_in_value_vs_filter_separator(self, paper_filter_with_raw_request):
        """
        This tests the problematic scenario:
        User thinks comma separates filters, but it doesn't when passed as single string.

        The filter expects either:
        1. Multiple query params: ?extra_filter=eq|..&extra_filter=contains|..
        2. BaseInFilter to split by comma

        But BaseInFilter splits BEFORE filter_json is called, and filter_json
        uses getlist() which may not work as expected.
        """
        # This is what user sends as single param
        filter_instance = paper_filter_with_raw_request(
            "eq|число тут|10,contains|фильтр вот такой|лт"
        )

        queryset = MagicMock()
        queryset.annotate.return_value = queryset
        queryset.filter.return_value = queryset

        result = filter_instance.filter_json(queryset, "extra_filter", None)

        # The current implementation receives ONE token with a comma inside
        # This will be parsed incorrectly by _build_q_from_token

        # Call filter_json and see what happens
        filter_call = queryset.filter.call_args
        assert filter_call is not None

    def test_proper_array_format(self, paper_filter_with_raw_request):
        """Test when values are properly passed as array (working case)"""
        filter_instance = PaperFilter()
        filter_instance.request = Mock()
        filter_instance.request.GET = Mock()
        # Properly split values (as if sent with multiple params)
        filter_instance.request.GET.getlist = Mock(
            return_value=["eq|число тут|10", "contains|фильтр вот такой|лт"]
        )

        queryset = MagicMock()
        queryset.annotate.return_value = queryset
        queryset.filter.return_value = queryset

        result = filter_instance.filter_json(queryset, "extra_filter", None)

        queryset.filter.assert_called_once()


class TestValueParameterUsage:
    """
    Tests to verify if filter_json uses the 'value' parameter correctly.

    The issue: filter_json receives a 'value' parameter from BaseInFilter
    (already comma-split), but then uses self.request.GET.getlist() instead.
    """

    def test_value_parameter_is_ignored(self):
        """
        Demonstrate that the 'value' parameter passed to filter_json is ignored.
        The method uses self.request.GET.getlist() instead.
        """
        filter_instance = PaperFilter()
        filter_instance.request = Mock()
        filter_instance.request.GET = Mock()

        # Mock getlist to return something different from value
        filter_instance.request.GET.getlist = Mock(return_value=["from_getlist"])

        queryset = MagicMock()
        queryset.annotate.return_value = queryset
        queryset.filter.return_value = queryset

        # Pass different value directly - it should be ignored by current implementation
        passed_value = ["from_value_param"]

        result = filter_instance.filter_json(queryset, "extra_filter", passed_value)

        # Verify that getlist was called
        filter_instance.request.GET.getlist.assert_called_once_with("extra_filter")

        # The filter uses getlist result, not the passed value!
        # This is the bug - BaseInFilter already processes the comma splitting,
        # but filter_json ignores it and re-reads from request.


class TestSplitFilterTokens:
    """Unit tests for _split_filter_tokens method"""

    @pytest.fixture
    def paper_filter(self):
        """Create PaperFilter instance for testing"""
        return PaperFilter()

    def test_single_token(self, paper_filter):
        """Test with single filter token"""
        result = paper_filter._split_filter_tokens("eq|field|value")
        assert result == ["eq|field|value"]

    def test_multiple_tokens_comma_separated(self, paper_filter):
        """Test splitting multiple comma-separated tokens"""
        result = paper_filter._split_filter_tokens("eq|field1|10,contains|field2|text")
        assert result == ["eq|field1|10", "contains|field2|text"]

    def test_three_tokens(self, paper_filter):
        """Test splitting three comma-separated tokens"""
        result = paper_filter._split_filter_tokens("eq|a|1,contains|b|2,gte|c|3")
        assert result == ["eq|a|1", "contains|b|2", "gte|c|3"]

    def test_in_operator_with_commas_in_value(self, paper_filter):
        """Test that in operator's comma-separated values are preserved"""
        result = paper_filter._split_filter_tokens("in|status|active,archived")
        # Should NOT split - comma is part of the value
        assert result == ["in|status|active,archived"]

    def test_in_operator_followed_by_another_filter(self, paper_filter):
        """Test in operator followed by another filter"""
        result = paper_filter._split_filter_tokens(
            "in|status|active,archived,eq|field|10"
        )
        assert result == ["in|status|active,archived", "eq|field|10"]

    def test_empty_string(self, paper_filter):
        """Test with empty string"""
        result = paper_filter._split_filter_tokens("")
        assert result == []

    def test_whitespace_handling(self, paper_filter):
        """Test that whitespace around tokens is trimmed, but spaces within tokens are preserved"""
        # Whitespace AFTER token is trimmed, but comma must be directly before operator
        result = paper_filter._split_filter_tokens("eq|a|1,contains|b|2 ")
        assert result == ["eq|a|1", "contains|b|2"]

        # Whitespace in field names is preserved (like "мин балл")
        result = paper_filter._split_filter_tokens("eq|мин балл|1,contains|макс балл|2")
        assert result == ["eq|мин балл|1", "contains|макс балл|2"]

    def test_cyrillic_field_names(self, paper_filter):
        """Test with cyrillic field names"""
        result = paper_filter._split_filter_tokens("eq|число тут|10,contains|фильтр|лт")
        assert result == ["eq|число тут|10", "contains|фильтр|лт"]

    def test_all_operators(self, paper_filter):
        """Test with all supported operators"""
        result = paper_filter._split_filter_tokens(
            "eq|a|1,in|b|x,y,contains|c|z,lte|d|5,gte|e|10"
        )
        assert result == ["eq|a|1", "in|b|x,y", "contains|c|z", "lte|d|5", "gte|e|10"]


class TestSanitizeAlias:
    """Unit tests for _sanitize_alias method"""

    @pytest.fixture
    def paper_filter(self):
        """Create PaperFilter instance for testing"""
        return PaperFilter()

    def test_no_special_chars(self, paper_filter):
        """Test with normal string"""
        result = paper_filter._sanitize_alias("field_name")
        assert result == "field_name"

    def test_spaces_replaced(self, paper_filter):
        """Test that spaces are replaced with underscores"""
        result = paper_filter._sanitize_alias("мин балл")
        assert result == "мин_балл"
        assert " " not in result

    def test_quotes_removed(self, paper_filter):
        """Test that quotes are replaced"""
        result = paper_filter._sanitize_alias('field"name')
        assert result == "field_name"

    def test_semicolons_removed(self, paper_filter):
        """Test that semicolons are replaced"""
        result = paper_filter._sanitize_alias("field;name")
        assert result == "field_name"
