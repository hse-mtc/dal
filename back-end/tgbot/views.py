from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.decorators import permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

from django_filters.rest_framework import DjangoFilterBackend

from tgbot.serializers import SessionSerializer
from tgbot.models import Session
from tgbot.filters import SessionFilter


class SessionViewSet(ModelViewSet):
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]

    filterset_class = SessionFilter


def create_codes():
    values = ['ckld']

    for value in values:
        session, _ = Session.objects.get_or_create(code=value)
        session.save()


# pylint: disable=(too-many-locals)
@api_view(['POST'])
@permission_classes((AllowAny,))
def populate(request: Request) -> Response:
    create_codes()

    return Response({'message': 'Population successful'},
                    status=HTTP_201_CREATED)
