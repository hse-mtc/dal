from rest_framework import serializers


class PopulateSerializer(serializers.Serializer):
    auth = serializers.BooleanField(write_only=True, default=True)
    common = serializers.BooleanField(write_only=True, default=True)
    dms = serializers.BooleanField(write_only=True, default=True)
    lms = serializers.BooleanField(write_only=True, default=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
