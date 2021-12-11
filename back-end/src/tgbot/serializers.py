from rest_framework.serializers import ModelSerializer

from tgbot.models import Session


class SessionSerializer(ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"
