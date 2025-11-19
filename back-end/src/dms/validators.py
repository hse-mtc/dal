from django.core.exceptions import ValidationError
from jsonschema import Draft7Validator, SchemaError


def validate_json_schema(value):
    """
    Validates that the provided value is a valid JSON Schema.

    Args:
        value: The value to validate (should be a dict representing JSON Schema)

    Raises:
        ValidationError: If the value is not a valid JSON Schema
    """
    if value is None:
        return

    try:
        # Try to create a validator with the provided schema
        # This will raise SchemaError if the schema is invalid
        Draft7Validator.check_schema(value)
    except SchemaError as e:
        raise ValidationError(
            f"Invalid JSON Schema: {str(e)}", code="invalid_json_schema"
        ) from e
    except Exception as e:
        raise ValidationError(
            f"Error validating JSON Schema: {str(e)}",
            code="json_schema_validation_error",
        ) from e
