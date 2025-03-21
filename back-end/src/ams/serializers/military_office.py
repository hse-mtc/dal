from rest_framework import serializers
from common.models.military import MilitaryOffice


class MilitaryOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilitaryOffice
        fields = ['id', 'name', 'city', 'code', 'is_custom']
