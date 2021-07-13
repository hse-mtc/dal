from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer

from drf_extra_fields.fields import Base64ImageField

from common.models.persons import (
    BirthInfo,
    ContactInfo,
    Relative,
    Photo,
)


class BirthInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = BirthInfo
        exclude = ["id"]


class ContactInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactInfo
        exclude = ["id"]


class PersonSerializer(serializers.ModelSerializer):
    birth_info = BirthInfoSerializer(read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)

    class Meta:
        abstract = True


class PersonMutateSerializer(serializers.ModelSerializer):
    birth_info = BirthInfoSerializer(required=False)
    contact_info = ContactInfoSerializer()

    class Meta:
        abstract = True


class RelativeSerializer(PersonSerializer):

    class Meta:
        model = Relative
        exclude = ["id"]


class RelativeMutateSerializer(
        WritableNestedModelSerializer,
        PersonMutateSerializer,
):

    class Meta:
        model = Relative
        exclude = ["id"]


class PersonnelMutateSerializer(PersonMutateSerializer):
    image = Base64ImageField(write_only=True, required=False)

    class Meta:
        exclude = ["photo"]

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
