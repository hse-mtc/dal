from rest_framework import serializers


class SearchPersonnelUsersSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PersonnelUsersSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    user_id = serializers.IntegerField(source="user.id")

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
