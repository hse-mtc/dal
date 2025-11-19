import pytest
from django.core.exceptions import ValidationError
from dms.validators import validate_json_schema


class TestValidateJsonSchema:
    """Tests for JSON Schema validator."""

    def test_valid_simple_schema(self):
        """Test that a valid simple JSON Schema passes validation."""
        valid_schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "number"}},
        }
        # Should not raise any exception
        validate_json_schema(valid_schema)

    def test_valid_complex_schema(self):
        """Test that a valid complex JSON Schema passes validation."""
        valid_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0},
                "address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"},
                    },
                    "required": ["city"],
                },
            },
            "required": ["name", "age"],
        }
        # Should not raise any exception
        validate_json_schema(valid_schema)

    def test_none_value(self):
        """Test that None value is allowed (for nullable fields)."""
        # Should not raise any exception
        validate_json_schema(None)

    def test_invalid_schema_wrong_type(self):
        """Test that invalid schema with wrong type raises ValidationError."""
        invalid_schema = {
            "type": "invalid_type",
            "properties": {"name": {"type": "string"}},
        }
        with pytest.raises(ValidationError) as exc_info:
            validate_json_schema(invalid_schema)

        assert "Invalid JSON Schema" in str(exc_info.value)
        assert exc_info.value.code == "invalid_json_schema"

    def test_invalid_schema_wrong_structure(self):
        """Test that schema with invalid structure raises ValidationError."""
        invalid_schema = {"type": "object", "properties": "should_be_object_not_string"}
        with pytest.raises(ValidationError) as exc_info:
            validate_json_schema(invalid_schema)

        assert "Invalid JSON Schema" in str(exc_info.value)
        assert exc_info.value.code == "invalid_json_schema"

    def test_empty_schema(self):
        """Test that empty schema is valid (accepts anything)."""
        empty_schema = {}
        # Should not raise any exception - empty schema is valid
        validate_json_schema(empty_schema)

    def test_schema_with_definitions(self):
        """Test that schema with definitions/references passes validation."""
        schema_with_refs = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "definitions": {
                "address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"},
                    },
                }
            },
            "type": "object",
            "properties": {
                "billing_address": {"$ref": "#/definitions/address"},
                "shipping_address": {"$ref": "#/definitions/address"},
            },
        }
        # Should not raise any exception
        validate_json_schema(schema_with_refs)
