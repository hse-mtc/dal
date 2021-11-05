import typing as tp

from django.db import (
    models,
    transaction,
)

Model = tp.TypeVar("Model", bound=models.Model, covariant=True)


def get_or_create(
    model: tp.Type[Model],
    **fields: dict[str, tp.Any],
) -> Model:
    """Get existing object of the model or create one.

    Args:
        model: class that inherits from `django.db.models.Model`.
        **fields: key-value pairs with field names and values.

    Returns:
        object of the model.
    """

    with transaction.atomic():
        if not model.objects.filter(**fields).exists():
            model.objects.create(**fields)

    return model.objects.filter(**fields).first()
