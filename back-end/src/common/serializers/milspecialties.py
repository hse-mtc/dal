from rest_framework import serializers

from common.models.milspecialties import Milspecialty


class MilspecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Milspecialty
        fields = "__all__"
