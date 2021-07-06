from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

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
