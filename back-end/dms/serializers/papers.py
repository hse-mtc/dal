from rest_framework import serializers

from taggit.models import Tag

from dms.models.papers import (
    Category,
    Paper,
)
from dms.serializers.common import (
    AuthorSerializer,
    PublisherSerializer,
)
from dms.serializers.documents import (
    DocumentSerializer,
    DocumentMutateSerializer,
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name


class TagListField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        return data.values_list("name", flat=True)


class PaperSerializer(DocumentSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    publishers = PublisherSerializer(many=True, read_only=True)
    tags = TagListField(required=False, read_only=True)

    class Meta:
        model = Paper
        fields = "__all__"


class PaperMutateSerializer(DocumentMutateSerializer):
    tags = TagListField(required=False)

    class Meta:
        model = Paper
        fields = "__all__"

    def create(self, validated_data):
        tags = validated_data.pop("tags", None)
        instance = super().create(validated_data)
        if tags:
            instance.tags.set(*tags)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.set(*tags, clear=True)
        return instance
