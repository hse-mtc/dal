from rest_framework import serializers

from drf_spectacular.utils import inline_serializer

from dms.models.books import (
    Book,
    Cover,
)
from dms.serializers.documents import (
    DocumentMutateSerializer,
    DocumentSerializer,
)
from dms.serializers.common import (
    AuthorSerializer,
    PublisherSerializer,
    SubjectSerializer,
)


class CoverSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        use_url=True,
        allow_null=True,
        required=False,
        read_only=True,
    )

    class Meta:
        model = Cover
        exclude = ["id"]


class BookSerializer(DocumentSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    publishers = PublisherSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    cover = CoverSerializer(read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookMutateSerializer(DocumentMutateSerializer):
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Book
        fields = "__all__"

    def create(self, validated_data):
        if image := validated_data.pop("image", None):
            cover = Cover.objects.create(image=image)
            validated_data["cover"] = cover
        return super().create(validated_data)

    def update(self, instance: Book, validated_data):
        if image := validated_data.pop("image", None):
            if instance.cover:
                instance.cover.image = image
                instance.cover.save()
            else:
                instance.cover = Cover.objects.create(image=image)
        return super().update(instance, validated_data)


BookMutateSerializerForSwagger = inline_serializer(
    name="BookMutateInline",
    fields={
        "content": serializers.FileField(),
        "image": serializers.ImageField(),
        "data": BookMutateSerializer(),
    },
)
