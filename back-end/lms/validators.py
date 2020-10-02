import typing as tp

from django.db.models import Model

from rest_framework.serializers import ValidationError


class PresentInDatabaseValidator:

    def __init__(self,
                 model: Model,
                 field: tp.Optional[str] = None):
        self.model = model
        self.field = field

    def __call__(self, value):
        if self.field is not None:
            # check if objects with model_param=value exist
            query_filter = {self.field: value}
        else:
            # check not by field, but by the whole data
            query_filter = value
        if not self.model.objects.filter(**query_filter).exists():
            if self.field is not None:
                raise ValidationError(
                    f'There are no objects with {self.field} = {value} '
                    f'in model {self.model.__name__}')
            raise ValidationError(
                f'There are no objects like {str(query_filter)} '
                f'in model {self.model.__name__}')
