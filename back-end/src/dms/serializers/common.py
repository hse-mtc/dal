from rest_framework import serializers

from auth.serializers import UserSerializer

from dms.models.common import (
    Author,
    Publisher,
)

from common.models.subjects import Subject


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "surname", "name", "patronymic"]


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    user = UserSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subject
        fields = "__all__"


class OrderUpdateSerializer(serializers.Serializer):
    to = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        instance.to(validated_data["to"])
        instance.save()
        return validated_data
