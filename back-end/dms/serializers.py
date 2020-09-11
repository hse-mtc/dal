from rest_framework import serializers

from dms.models import (Author, Category)


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
