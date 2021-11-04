from abc import ABC

from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer

from drf_extra_fields.fields import Base64ImageField

from common.models.personal import (
    BirthInfo,
    ContactInfo,
    Name,
    Passport,
    Photo,
    Relative,
)


class NameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Name
        exclude = ["id"]


class BirthInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = BirthInfo
        exclude = ["id"]


class ContactInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactInfo
        exclude = ["id"]


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        use_url=True,
        allow_null=True,
        required=False,
        read_only=True,
    )

    class Meta:
        model = Photo
        exclude = ["id"]


class PhotoMutateMixin(serializers.Serializer, ABC):
    image = Base64ImageField(write_only=True, required=False)

    def create_photo(self, validated_data):
        image = validated_data.pop("image", None)
        if image is None:
            return

        photo = Photo.objects.create(image=image)
        validated_data["photo"] = photo

    def update_photo(self, instance, validated_data):
        if "image" not in validated_data:
            return

        if instance.photo:
            instance.photo.delete()

        self.create_photo(validated_data)


class PassportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passport
        exclude = ["id"]


class RelativeSerializer(serializers.ModelSerializer):
    name = NameSerializer(read_only=True)
    birth_info = BirthInfoSerializer(read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)

    class Meta:
        model = Relative
        exclude = ["id"]


class RelativeMutateSerializer(WritableNestedModelSerializer):

    class Meta:
        model = Relative
        exclude = ["id"]
