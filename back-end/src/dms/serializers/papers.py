from rest_framework import serializers

from taggit.models import Tag

from drf_spectacular.utils import inline_serializer

from dms.models.papers import (
    Category,
    Paper,
)
from dms.serializers.documents import (
    DocumentMutateSerializer,
    DocumentSerializer,
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
            instance.tags.set(tags)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.set(tags, clear=True)
        return instance


PaperMutateSerializerForSwagger = inline_serializer(
    name="PaperMutateInline",
    fields={
        "content": serializers.FileField(),
        "data": PaperMutateSerializer(),
    },
)
