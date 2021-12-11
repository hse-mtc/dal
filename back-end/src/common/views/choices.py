from rest_framework import permissions
from rest_framework import views
from rest_framework import serializers

from rest_framework.request import Request
from rest_framework.response import Response

from drf_spectacular.utils import inline_serializer


class ChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class GenericChoicesList(views.APIView):
    choices_class = None

    permission_classes = [permissions.AllowAny]

    def get_serializer(self):
        serializer = inline_serializer(
            name=self.__class__.__name__ + "Serializer",
            fields={choice.name: ChoiceSerializer() for choice in self.choices_class},
        )
        return serializer

    def make_choices(self, *args, **kwargs) -> dict:
        return {
            choice.name: {
                "value": choice.value,
                "label": choice.label,
            }
            for choice in self.choices_class
        }

    def get(self, request: Request, *args, **kwargs) -> Response:
        choices = self.make_choices()
        return Response(data=choices)
