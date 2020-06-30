from django.db.models import Model

from rest_framework.serializers import ValidationError


class PresentInDatasetValidator(object):
    def __init__(self, model_class: Model, model_param: str):
        self.model_class = model_class
        self.model_param = model_param

    def __call__(self, value):
        # check if objects with model_param=value exist
        query_filter = {self.model_param: value}
        if not self.model_class.objects.filter(**query_filter).exists():
            raise ValidationError(f'There are no objects with {self.model_param} = {value} in model {self.model_class.__name__}')
