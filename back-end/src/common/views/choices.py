from rest_framework import permissions
from rest_framework import views

from rest_framework.request import Request
from rest_framework.response import Response


class GenericChoicesList(views.APIView):
    choices_class = None

    permission_classes = [permissions.AllowAny]

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
