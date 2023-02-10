from rest_framework import serializers

from drf_spectacular.utils import inline_serializer

from auth.serializers import UserSerializer

from dms.models.books import (
    Book,
    Cover,
    FavoriteBook,
)
from dms.serializers.documents import (
    DocumentMutateSerializer,
    DocumentSerializer,
)


class CoverSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        use_url=False,
        allow_null=True,
        required=False,
        read_only=True,
    )

    class Meta:
        model = Cover
        exclude = ["id"]


class BookSerializer(DocumentSerializer):
    cover = CoverSerializer(read_only=True)
    favorite = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source="user.id")

    def get_favorite(self, obj: Book) -> bool:
        user_id = self.context["request"].user.id
        return obj.favoritebook_set.filter(user=user_id).exists()

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


class FavoriteBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = FavoriteBook
        fields = "__all__"

    # TODO: help Swagger deduce response schema
    def to_representation(self, instance: FavoriteBook):
        representation = super().to_representation(instance)
        return representation["book"]


class FavoriteBookMutateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBook
        fields = "__all__"
