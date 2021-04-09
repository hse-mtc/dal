from rest_framework import serializers


class PersonsQuerySerializer(serializers.Serializer):
    name = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
