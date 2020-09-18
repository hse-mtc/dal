from rest_framework import serializers

from taggit.models import Tag

from dms.models import (
    Author,
    Document,
    Category,
    Publisher,
    Subject,
    File,
)


class AuthorSerializer(serializers.ModelSerializer):
    """Serializes Author model."""

    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """Serializes Category model."""

    class Meta:
        model = Category
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):
    """Serializes Publisher model."""

    class Meta:
        model = Publisher
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    """Serializes Subject model."""

    class Meta:
        model = Subject
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """Serializes Tag model."""

    class Meta:
        model = Tag
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name


class TagListField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        return data.values_list("name", flat=True)


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        exclude = ["content"]

    extension = serializers.CharField(source="get_file_extension",
                                      required=False,
                                      read_only=True)

    name = serializers.CharField(source="get_file_name",
                                 required=False,
                                 read_only=True)


class DocumentSerializer(serializers.ModelSerializer):
    """Serializes Document model."""

    tags = TagListField(required=False)
    file = FileSerializer()

    class Meta:
        model = Document
        exclude = ["is_in_trash"]

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


class DocumentListSerializer(serializers.ModelSerializer):
    """Serializes a list of Document models."""

    authors = AuthorSerializer(many=True, read_only=True)
    publishers = PublisherSerializer(many=True, read_only=True)
    tags = TagListField(required=False, read_only=True)
    file = FileSerializer()

    class Meta:
        model = Document
        exclude = ["is_in_trash", "subject", "topic"]
