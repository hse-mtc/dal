from rest_framework import serializers

from dms.models import (
    Author,
    Category,
    Publisher,
    Subject,
)


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author model.
    """

    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializes Category model.
    """

    class Meta:
        model = Category
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializes Publisher model.
    """

    class Meta:
        model = Publisher
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializes Subject model.
    """

    class Meta:
        model = Subject
        fields = "__all__"
